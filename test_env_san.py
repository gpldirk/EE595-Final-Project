# Parameters
num_clus = 2	
serv_per_clus = 5
cpu_per_serv = 64 # Virtual cores (2* phys = virt)
mem_per_serv = 128 # Memory should always be cores * 2
		
# Additional variables calculated with parameters
serv_total = num_clus*serv_per_clus
	
# VMs, sm = 1 vcore, 2 GB; md = 2 vcore, 4GB; lg = 4 vcore, 8GB
sm = round(cpu_per_serv*.5) # 50% of the server are small VMs
md = round(cpu_per_serv*.3) # 30% of the server are medium VMs
lg = cpu_per_serv - (sm+md) # 20% of the server are large VMs

# Dictionary initializing the VMs within the server
vm_ind = {
	'sm': sm,
	'md': md,
	'lg': lg
}
#print(vm_ind)

# The vm dictionary is nested within the server dictionary
servers = {}
servlist = []
for i in range(0,serv_total):
	servers.update({i: vm_ind}) 
	servlist.append(i)
#print(servers)
#print(servlist)

# The clusters are saved within a list. 
# Example, if I want to access the third server in the second cluster: servers[clusters[1][2]]
clusters = []
for i in range(0,num_clus):
	begin = i*serv_per_clus
	end = begin+serv_per_clus
	clusters.append(servlist[begin:end])
#print(clusters)
