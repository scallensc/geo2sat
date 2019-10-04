import yaml

class API_KEY:
    ''' Retrieve API keys from file '''
    def get(self):
        ''' Load API keys or display error if file not found '''
        try:
            with open('apikeys.yaml', 'r') as config_file:
                config = yaml.load(config_file)
                return config['apikeys'][self]
        except FileNotFoundError:
            print("'%s' file not found" % self)