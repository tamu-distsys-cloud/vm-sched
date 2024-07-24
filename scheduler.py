from vm import VM
from vmi import VMI


class Scheduler:
    def __init__(self):
        self.vmi = VMI()
    
    def attach(self, vm: VM):
        npages = self.vmi.count_unique_pages(vm)
        print("New VM attached: %d pages used" % npages)
