from __future__ import annotations

import dataclasses
import hashlib
import hmac
import os
import secrets
from typing import Dict, Iterable, List, Optional, Set


BASE_ROLES = {
    "administracion",
    "compras",
    "produccion",
    "ventas",
    "almacen",
}


@dataclasses.dataclass(frozen=True)
class PermissionSet:
    module: str
    actions: Set[str]


class RolePermissions:
    """Stores module-level permissions for each role."""

    def __init__(self, base_roles: Iterable[str] = BASE_ROLES) -> None:
        self._roles: Dict[str, Dict[str, Set[str]]] = {
            role: {} for role in base_roles
        }

    def configure_module(self, role: str, module: str, actions: Iterable[str]) -> None:
        self._ensure_role(role)
        self._roles[role][module] = set(actions)

    def grant_action(self, role: str, module: str, action: str) -> None:
        self._ensure_role(role)
        self._roles[role].setdefault(module, set()).add(action)

    def revoke_action(self, role: str, module: str, action: str) -> None:
        self._ensure_role(role)
        if module in self._roles[role]:
            self._roles[role][module].discard(action)

    def allowed_actions(self, role: str, module: str) -> Set[str]:
        self._ensure_role(role)
        return set(self._roles[role].get(module, set()))

    def permissions_for_role(self, role: str) -> List[PermissionSet]:
        self._ensure_role(role)
        return [
            PermissionSet(module=module, actions=set(actions))
            for module, actions in self._roles[role].items()
        ]

    def _ensure_role(self, role: str) -> None:
        if role not in self._roles:
            raise ValueError(f"Rol desconocido: {role}")


@dataclasses.dataclass
class User:
    username: str
    role: str
    password_hash: str
    salt: str

    def verify_password(self, password: str) -> bool:
        candidate = _hash_password(password, bytes.fromhex(self.salt))
        return hmac.compare_digest(self.password_hash, candidate)


class AuthService:
    """Simple user/password authentication with PBKDF2 hashing."""

    def __init__(self, permissions: RolePermissions) -> None:
        self._permissions = permissions
        self._users: Dict[str, User] = {}

    def register_user(self, username: str, password: str, role: str) -> User:
        if username in self._users:
            raise ValueError("El usuario ya existe.")
        self._permissions._ensure_role(role)
        salt = os.urandom(16)
        password_hash = _hash_password(password, salt)
        user = User(
            username=username,
            role=role,
            password_hash=password_hash,
            salt=salt.hex(),
        )
        self._users[username] = user
        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self._users.get(username)
        if not user:
            return None
        if user.verify_password(password):
            return user
        return None

    def allowed_actions(self, user: User, module: str) -> Set[str]:
        return self._permissions.allowed_actions(user.role, module)


@dataclasses.dataclass(frozen=True)
class AuditEvent:
    actor: str
    action: str
    module: str
    metadata: Dict[str, str]


class AuditLogger:
    """Collects sensitive action events in memory."""

    def __init__(self) -> None:
        self._events: List[AuditEvent] = []

    def record_sensitive_action(
        self,
        actor: User,
        module: str,
        action: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> AuditEvent:
        event = AuditEvent(
            actor=actor.username,
            action=action,
            module=module,
            metadata=metadata or {},
        )
        self._events.append(event)
        return event

    def list_events(self) -> List[AuditEvent]:
        return list(self._events)


SENSITIVE_ACTIONS = {
    "crear_orden",
    "aprobar_compra",
    "cancelar_produccion",
    "ajustar_inventario",
    "eliminar_factura",
}


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000).hex()


def perform_action(
    user: User,
    module: str,
    action: str,
    permissions: RolePermissions,
    audit: AuditLogger,
    metadata: Optional[Dict[str, str]] = None,
) -> bool:
    """Execute an action if permitted, writing to audit log when sensitive."""

    allowed = permissions.allowed_actions(user.role, module)
    if action not in allowed:
        return False

    if action in SENSITIVE_ACTIONS:
        audit.record_sensitive_action(user, module, action, metadata)
    return True
