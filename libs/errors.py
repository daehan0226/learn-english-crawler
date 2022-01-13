class NoKeywordArgsError(Exception):
    def __init__(self, key, message="Missing keyword"):
        self.key = key
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}, key name : {self.key}"


class WrongRunCommandError(Exception):
    def __init__(self, key):
        keyword_type_list = ["phrasal_verbs", "idioms"]
        env_list = ["server", "dev"]
        self.key = key
        self.message = f"""
            kwargs=
                keywords must not include space, replace space with hyphen if they include space
                keyword_type must be one of {", ".join(keyword_type_list)}
                env must be one of {", ".join(env_list)}
        
            Run command should be like
                python .\main.py keyword='keyword1,keyword2', keyword_type='keyword_type' env='env'
        
        """
        super().__init__(self.message)
