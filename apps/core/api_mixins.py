from rest_framework import viewsets


class ActionPermissionMixin:
    permission_classes_by_action = {}

    def get_permissions(self):
        permission_classes = self.permission_classes_by_action.get(
            getattr(self, "action", None),
            getattr(self, "permission_classes", []),
        )
        return [permission() for permission in permission_classes]


class ReadWriteSerializerMixin:
    read_serializer_class = None
    write_serializer_class = None
    serializer_action_classes = {}

    def get_read_serializer_class(self):
        return self.read_serializer_class or super().get_serializer_class()

    def get_write_serializer_class(self):
        return self.write_serializer_class or self.get_read_serializer_class()

    def get_serializer_class(self):
        action = getattr(self, "action", None)
        if action in self.serializer_action_classes:
            return self.serializer_action_classes[action]
        if action in {"create", "update", "partial_update"} and self.write_serializer_class:
            return self.get_write_serializer_class()
        if self.read_serializer_class:
            return self.get_read_serializer_class()
        return super().get_serializer_class()

    def get_read_serializer(self, *args, **kwargs):
        serializer_class = self.get_read_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_write_serializer(self, *args, **kwargs):
        serializer_class = self.get_write_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class ActionThrottleMixin:
    throttle_classes_by_action = {}
    throttle_scopes_by_action = {}

    def get_throttles(self):
        action = getattr(self, "action", None)
        if action in self.throttle_scopes_by_action:
            self.throttle_scope = self.throttle_scopes_by_action[action]
        throttle_classes = self.throttle_classes_by_action.get(action)
        if throttle_classes is None:
            return super().get_throttles()
        return [throttle() for throttle in throttle_classes]


class ManagedModelViewSet(
    ActionPermissionMixin,
    ActionThrottleMixin,
    ReadWriteSerializerMixin,
    viewsets.ModelViewSet,
):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
