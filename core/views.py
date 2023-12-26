from rest_framework import viewsets


class ActionSerializedViewSet(viewsets.ModelViewSet):
    action_serializers = {}
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return self.serializer_class