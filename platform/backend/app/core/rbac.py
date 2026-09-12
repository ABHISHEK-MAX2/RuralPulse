from enum import Enum


class Role(str, Enum):
    DISTRICT_HEALTH_OFFICER = "district_health_officer"
    MMU_COORDINATOR = "mmu_coordinator"
    STATE_HEALTH_ADMINISTRATOR = "state_health_administrator"
    SYSTEM_ADMINISTRATOR = "system_administrator"


NAV_BY_ROLE = {
    Role.DISTRICT_HEALTH_OFFICER: ["dashboard", "villages", "map", "facilities", "alerts", "reports"],
    Role.MMU_COORDINATOR: ["dashboard", "mmu", "map", "villages", "alerts"],
    Role.STATE_HEALTH_ADMINISTRATOR: ["dashboard", "analytics", "map", "villages", "facilities", "mmu", "reports", "data_sources"],
    Role.SYSTEM_ADMINISTRATOR: ["dashboard", "admin", "data_sources", "analytics", "villages", "facilities", "mmu", "reports"],
}


PERMISSIONS_BY_ROLE = {
    Role.DISTRICT_HEALTH_OFFICER: {"scope": "district", "can_edit_mmu_schedule": True, "can_manage_users": False},
    Role.MMU_COORDINATOR: {"scope": "district", "can_edit_mmu_schedule": True, "can_manage_users": False},
    Role.STATE_HEALTH_ADMINISTRATOR: {"scope": "state", "can_edit_mmu_schedule": False, "can_manage_users": False},
    Role.SYSTEM_ADMINISTRATOR: {"scope": "system", "can_edit_mmu_schedule": True, "can_manage_users": True},
}
