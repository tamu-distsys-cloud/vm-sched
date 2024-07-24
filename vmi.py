from vm import VM

KERNEL_BASE = 0xc0000000

KERNEL_SYMBOLS = {
        "init_task": 0xc0958300,
    }

TASK_STRUCT_OFFSET = {
        "tasks.next": 668,
        "comm":       0,    # TODO: Find out the offset of comm in task_struct
        "mm":         708,
    }

MM_STRUCT_OFFSET = {
        "pgd":        28,
    }

class VMI:
    def __init__(self):
        # Put your code here if necessary
        pass

    def list_process_names(self, vm: VM):
        # TODO: Finish this function
        return []

    def list_pgtables(self, vm: VM):
        # TODO: Finish this function
        return []

    def count_unique_pages(self, vm: VM, pgtable):
        # TODO: Finish this function
        pass
