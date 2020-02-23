

class ModelMixin:
    def to_dict(self):
        model_dict = {}
        for field in self._meta.get_fields():
            model_dict[field.attname] = getattr(self, field.attname, None)

        return model_dict