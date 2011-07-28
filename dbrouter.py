class GeocodeCacheRouter(object):
    """A router to control all database operations on models in
    the geocodecache application"""

    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'geocodecache':
            return 'geocode'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'geocodecache':
            return 'geocode'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        return None


    def allow_syncdb(self, db, model):
        allowed = ['south']
        if model._meta.app_label in allowed:
            return True
        elif db == 'geocode':
            return model._meta.app_label == 'geocodecache'
        elif model._meta.app_label == 'geocodecache':
            return False
        return None
        
        #"Make sure the myapp app only appears on the 'other' db"
        #if db == 'geocode':
        #    return model._meta.app_label == 'geocodecache'
        #elif model._meta.app_label == 'geocodecache':
        #    return False
        #return None
