from vm import VM
from vmi import VMI


class Scheduler:
    def __init__(self, host_capacities):
        self.vmi = VMI()
        self.num_hosts = len(host_capacities)
        self.host_capacities = host_capacities
        self.hosted_vms = [[]] * num_hosts

    def host_usage(self):
        usages = [0] * self.num_hosts
        for i in range(self.num_hosts):
            usage[i] = 0
            for vm in self.hosted_vms:
                usage[i] += vm.mem_usage()
        return usages

    def attach(self, vm: VM):
        npages = self.vmi.count_unique_pages(vm)
        print("New VM attached: %d pages used" % npages)

        # TODO: Finish this function
