provider "aws" {}

resource "aws_vpc" "tf-test-vpc" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name: "${var.env_prefix}-vpc"
  }
}

module "tf-test-subnet" {
  source = "./modules/subnet"
  subnet_cidr_block = var.subnet_cidr_block
  avail_zone = var.avail_zone
  env_prefix = var.env_prefix
  aws_vpc = aws_vpc.tf-test-vpc
}

module "tf-test-aws_instance" {
  source = "./modules/ec2-instance"
  instance_count = var.instance_count
  my_ips = var.my_ips
  env_prefix = var.env_prefix
  public_key_location = var.public_key_location
  private_key_location = var.private_key_location
  instance_type = var.instance_type
  avail_zone = var.avail_zone
  subnet_id = module.tf-test-subnet.aws_subnet.id
  aws_vpc = aws_vpc.tf-test-vpc
}
