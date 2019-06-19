from config import _YML_HEADER, _YML_FOOTER, \
    _SSH_INIT_YML_NODE_FORMAT, _STARTER_MASTER_NODE_FORMAT, _STARTER_SLAVE_NODE_FORMAT,\
    SSH_INIT_COMPOSE_YML_PATH, STARTER_COMPOSE_YML_PATH


class BaseTemplate(object):
    required_keys = ["node_name", "image", "node_ssh_dir"]
    # 可选的KEY，如果不提供，讲指定的KEY的值作为他们的默认值，如下面讲service_name作为主机名称和容器名称的默认值
    options_keys = {
        "hostname": "node_name",
        "container_name": "node_name"
    }

    YML_NAME = None

    def __init__(self, nodes_config):

        self.version = "3.7" if "version" not in nodes_config else nodes_config["version"]

        self.nodes_config = [nodes_config["master"]] + nodes_config["slaves"]

        for node_config in self.nodes_config:
            for req_key in self.required_keys:
                if req_key not in node_config:
                    raise Exception("缺失必要参数：{}. 必须提供：{}".format(req_key, self.required_keys))
            for opt_key, default_key in self.options_keys.items():
                if opt_key not in node_config:
                    node_config[opt_key] = node_config[default_key]

    def create(self):
        yml_data = self.generate()
        with open(self.YML_NAME, "w") as f:
            f.write(yml_data)

    def generate(self):
        pass

class SSHInitYamlTemplate(BaseTemplate):

    YML_NAME = SSH_INIT_COMPOSE_YML_PATH

    def generate(self):
        '''生成YML配置文件数据'''
        yml_data = _YML_HEADER.format(version=self.version)
        for node_config in self.nodes_config:
            yml_data += _SSH_INIT_YML_NODE_FORMAT.format(
                   node_name=node_config["node_name"],
                   image=node_config["image"],
                   hostname=node_config["hostname"],
                   container_name=node_config["container_name"],
                   node_ssh_dir=node_config["node_ssh_dir"]
               )
        yml_data += _YML_FOOTER

        return yml_data

    def __str__(self):
        return self.generate()


class StarterYamlTemplate(SSHInitYamlTemplate):

    YML_NAME = STARTER_COMPOSE_YML_PATH

    def __init__(self, *args, **kwaegs):
        self.required_keys += ["hadoop_config_dir", "hadoop_data_dir"]
        super(StarterYamlTemplate, self).__init__(*args, **kwaegs)

    def generate(self):
        '''生成YML配置文件数据'''
        yml_data = _YML_HEADER.format(version=self.version)

        # Master节点配置
        node_config = self.nodes_config[0]
        yml_data += _STARTER_MASTER_NODE_FORMAT.format(
            node_name=node_config["node_name"],
            image=node_config["image"],
            hostname=node_config["hostname"],
            container_name=node_config["container_name"],
            node_ssh_dir=node_config["node_ssh_dir"],
            hadoop_config_dir=node_config["hadoop_config_dir"],
            hadoop_data_dir=node_config["hadoop_data_dir"]
        )
        # Slave节点配置
        for node_config in self.nodes_config[1:]:
            yml_data += _STARTER_SLAVE_NODE_FORMAT.format(
                node_name=node_config["node_name"],
                image=node_config["image"],
                hostname=node_config["hostname"],
                container_name=node_config["container_name"],
                node_ssh_dir=node_config["node_ssh_dir"],
                hadoop_config_dir=node_config["hadoop_config_dir"],
                hadoop_data_dir=node_config["hadoop_data_dir"]
            )
        yml_data += _YML_FOOTER

        return yml_data


if __name__ == '__main__':
    from config import CLUSTER_CONFIG_TEMPLATE

    obj = SSHInitYamlTemplate(CLUSTER_CONFIG_TEMPLATE)
    print(obj.generate())

    obj = StarterYamlTemplate(CLUSTER_CONFIG_TEMPLATE)
    print(obj.generate())