from rest_framework import serializers

class BasePathSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    def get_url(self, obj):      
       return "/api/%s/%i/" % (self.get_path() , obj.id)
    
    def get_home_path(self):      
       return "/api/%s/" % self.get_path()
    
    @classmethod
    def get_path(cls):
        raise NotImplementedError("'get_path' method should be implemented in '%s' class" % cls.__name__)
        