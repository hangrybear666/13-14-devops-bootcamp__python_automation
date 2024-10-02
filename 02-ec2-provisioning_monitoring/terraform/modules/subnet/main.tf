resource "aws_subnet" "tf-test-subnet-1" {
  vpc_id = var.aws_vpc.id
  cidr_block = var.subnet_cidr_block
  availability_zone = var.avail_zone
  tags = {
    Name: "${var.env_prefix}-subnet-1"
  }
}

resource "aws_internet_gateway" "tf-test-igw" {
  vpc_id = var.aws_vpc.id
  tags = {
    Name: "${var.env_prefix}-igw"
  }
}

/*
// Alternative to explicit aws_route_table in which case we can delete the aws_route_table_association since all unassigned subnets automatically get assigned to the default/main route table
resource "aws_default_route_table" "main-rtb" {
  default_route_table_id = aws_vpc.tf-test-vpc.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.tf-test-igw.id
  }
  tags = {
    Name: "${var.env_prefix}-main-rtb"
  }
}
*/
resource "aws_route_table" "tf-test-route-table" {
  vpc_id = var.aws_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.tf-test-igw.id
  }
  tags = {
    Name: "${var.env_prefix}-route-table"
  }
}

resource "aws_route_table_association" "rtb-subnet-association" {
  subnet_id = aws_subnet.tf-test-subnet-1.id
  route_table_id = aws_route_table.tf-test-route-table.id
}