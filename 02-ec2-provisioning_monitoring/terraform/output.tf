output "debian_12_ami_id" {
  # value = module.tf-test-aws_instance.debian_12_ami
  value = module.tf-test-aws_instance.debian_12_ami.id
}
output "ec2-public_ips" {
  value = [for instance in module.tf-test-aws_instance.ec2-instance : instance.public_ip]
  description = "List of public IPs of the EC2 instances"
}

output "ec2-ssh-commands" {
  value = [for instance in module.tf-test-aws_instance.ec2-instance : "ssh -i ${var.private_key_location} admin@${instance.public_ip}"]
  description = "List of SSH commands for accessing the EC2 instances"
}

