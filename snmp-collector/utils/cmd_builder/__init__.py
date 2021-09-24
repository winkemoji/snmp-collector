class CmdBuilderBase(object):
    def __init__(self):
        self._options = {
            "-v": "",
            "-c": "",
            "-u": "",
            "-l": "",
            "-a": "",
            "-A": "",
            "-e": "",
            "-E": "",
            "-n": "",
            "-x": "",
            "-X": "",
            "-Z": "",
            "-r": "",
            "-t": "",
        }
        self._agent = ""
        self._oids = []
        pass

    def set_agent(self, agent):
        raise NotImplementedError()

    def set_oid(self, oid):
        raise NotImplementedError()

    def set_version(self, version):
        raise NotImplementedError()

    def set_username(self, username):
        raise NotImplementedError()

    def set_community(self, community):
        raise NotImplementedError()

    def set_auth_protocol(self, auth_protocol):
        raise NotImplementedError()

    def set_auth_pass(self, auth_pass):
        raise NotImplementedError()

    def set_security_engine_id(self, security_engine_id):
        raise NotImplementedError()

    def set_context_engine_id(self, context_engine_id):
        raise NotImplementedError()

    def set_security_level(self, security_level):
        raise NotImplementedError()

    def set_context(self, context):
        raise NotImplementedError()

    def set_priv_protocol(self, priv_protocol):
        raise NotImplementedError()

    def set_priv_pass(self, priv_pass):
        raise NotImplementedError()

    def set_boots_time(self, boots_time):
        raise NotImplementedError()

    def set_retries(self, retries):
        raise NotImplementedError()

    def set_timeout(self, timeout):
        raise NotImplementedError()



class GetCmdBuilder(CmdBuilderBase):

    def __init__(self):
        super(GetCmdBuilder, self).__init__()

    def set_agent(self, agent):
        self._agent = agent
        return self

    def set_oid(self, oid):
        if isinstance(oid, list):
            self._oids += oid
        else:
            self._oids.append(oid)
        return self

    def set_version(self, version):
        self._options['-v'] = version
        return self

    def set_username(self, username):
        self._options['-u'] = username
        return self

    def set_community(self, community):
        self._options['-c'] = community
        return self

    def set_auth_protocol(self, auth_protocol):
        self._options['-a'] = auth_protocol
        return self

    def set_auth_pass(self, auth_pass):
        self._options['-A'] = auth_pass
        return self

    def set_security_engine_id(self, security_engine_id):
        self._options['-e'] = security_engine_id
        return self

    def set_context_engine_id(self, context_engine_id):
        self._options['-E'] = context_engine_id
        return self

    def set_security_level(self, security_level):
        self._options['-l'] = security_level
        return self

    def set_context(self, context):
        self._options['-n'] = context
        return self

    def set_priv_protocol(self, priv_protocol):
        self._options['-x'] = priv_protocol
        return self

    def set_priv_pass(self, priv_pass):
        self._options['-X'] = priv_pass
        return self

    def set_boots_time(self, boots_time):
        self._options['-Z'] = boots_time
        return self

    def set_retries(self, retries):
        self._options['-r'] = retries
        return self

    def set_timeout(self, timeout):
        self._options['-t'] = timeout
        return self

    def get_options(self):
        return self._options

    def get_oid(self):
        return self._oids

    def get_agent(self):
        return self._agent

    def build(self):
        """
        USAGE: snmpget [OPTIONS] AGENT OID [OID]...
        """
        empty_options = [k for k, v in self._options.items() if len(v.strip()) == 0]
        for option in empty_options:
            self._options.pop(option)
        option_list = convert_options_dict_to_list(self._options)
        return ['snmpget'] + option_list + [self._agent] + self._oids



class WalkCmdBuilder(CmdBuilderBase):

    def __init__(self):
        super(WalkCmdBuilder, self).__init__()

    def set_agent(self, agent):
        self._agent = agent
        return self

    def set_oid(self, oid):
        self._oids = oid
        return self

    def set_version(self, version):
        self._options['-v'] = version
        return self

    def set_username(self, username):
        self._options['-u'] = username
        return self

    def set_community(self, community):
        self._options['-c'] = community
        return self

    def set_auth_protocol(self, auth_protocol):
        self._options['-a'] = auth_protocol
        return self

    def set_auth_pass(self, auth_pass):
        self._options['-A'] = auth_pass
        return self

    def set_security_engine_id(self, security_engine_id):
        self._options['-e'] = security_engine_id
        return self

    def set_context_engine_id(self, context_engine_id):
        self._options['-E'] = context_engine_id
        return self

    def set_security_level(self, security_level):
        self._options['-l'] = security_level
        return self

    def set_context(self, context):
        self._options['-n'] = context
        return self

    def set_priv_protocol(self, priv_protocol):
        self._options['-x'] = priv_protocol
        return self

    def set_priv_pass(self, priv_pass):
        self._options['-X'] = priv_pass
        return self

    def set_boots_time(self, boots_time):
        self._options['-Z'] = boots_time
        return self

    def set_retries(self, retries):
        self._options['-r'] = retries
        return self

    def set_timeout(self, timeout):
        self._options['-t'] = timeout
        return self

    def get_options(self):
        return self._options

    def get_oid(self):
        return self._oids

    def get_agent(self):
        return self._agent

    def build(self):
        """
        USAGE: snmpwalk [OPTIONS] AGENT [OID]
        """
        empty_options = [k for k, v in self._options.items() if len(v.strip()) == 0]
        for option in empty_options:
            self._options.pop(option)
        option_list = convert_options_dict_to_list(self._options)
        return ['snmpwalk'] + option_list + [self._agent] + [self._oids]



class Version:
    def __init__(self):
        self.V1 = "1"
        self.V2 = "2c"
        self.V3 = "3"


class AuthProtocol:
    def __init__(self):
        self.MD5 = "MD5"
        self.SHA = "SHA"
        self.SHA_224 = "SHA-224"
        self.SHA_256 = "SHA-256"
        self.SHA_384 = "SHA-384"
        self.SHA_512 = "SHA-512"


class PrivProtocol:
    def __init__(self):
        self.DES = "DES"
        self.AES = "AES"


class SecurityLevel:
    def __init__(self):
        self.noAuthNoPriv = "noAuthNoPriv"
        self.authNoPriv = "authNoPriv"
        self.authPriv = "authPriv"


version = Version()
authProtocol = AuthProtocol()
privProtocol = PrivProtocol()
securityLevel = SecurityLevel()



def convert_options_dict_to_list(options_dict):
    """
    参数的字典(options_dict) 转换为列表(options-list)
    :param options_dict:  :return:
    """
    options_list_len = len(options_dict) * 2
    options_list = [""] * options_list_len
    k = iter(list(options_dict))
    v = iter(list(options_dict.values()))
    for i in range(options_list_len):
        if i % 2 == 0:
            options_list[i] = next(k)
        else:
            options_list[i] = next(v)
    return options_list
