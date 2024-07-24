from vm import VM

KERNEL_BASE = 0xc0000000

KERNEL_SYMBOLS = {
        "init_task": 0xc0958300,
    }

TASK_STRUCT_OFFSET = {
        "tasks.next": 668,
        "comm":       0,    # TODO: find the offset of comm in task_struct
        "mm":         708,
    }

MM_STRUCT_OFFSET = {
        "pgd":        28,
    }

class VMI:
    def __init__(self):
        pass

    def list_process_names(self, vm: VM):
        return []

    def list_pgtables(self, vm: VM):
        return []

    def count_unique_pages(self, vm: VM, pgtable):
        pass
