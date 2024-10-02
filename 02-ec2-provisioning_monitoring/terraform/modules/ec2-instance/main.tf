
resource "aws_default_security_group" "default-sg" {
  vpc_id = var.aws_vpc.id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "TCP"
    cidr_blocks = var.my_ips
  }

  # ingress {
  #   from_port = 8080
  #   to_port = 8080
  #   protocol = "TCP"
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    prefix_list_ids = []
  }

  tags = {
    Name: "${var.env_prefix}-default-sg"
  }
}

data "aws_ami" "debian-12-image" {
  most_recent = true
  owners      = ["136693071363"]  # Debian's official AWS account ID

  filter {
    name   = "name"
    values = ["debian-12-amd64-*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

resource "aws_key_pair" "ssh-key" {
  key_name = "tf-server-key"
  public_key = file(var.public_key_location)
}

resource "aws_instance" "tf-test-server" {
  ami = data.aws_ami.debian-12-image.id
  instance_type = var.instance_type
  count = var.instance_count

  subnet_id = var.subnet_id
  vpc_security_group_ids = [aws_default_security_group.default-sg.id]
  availability_zone = var.avail_zone

  associate_public_ip_address = true
  key_name = aws_key_pair.ssh-key.key_name

  # alternative is to use an existing key from AWS and use its respective private key .pem file to ssh into the server
  # key_name ="hangrybear_dev-one"

  # the problem with user data is no logging in terraform, it is also not possible to pass multiple files
  # user_data = file("payload/install-git-on-debian-ec2.sh")

  user_data_replace_on_change = true
  // WARNING: Provisioners are NOT recommended by terraform as it breaks the principle of idempotency
  connection {
    type = "ssh"
    host = self.public_ip
    user = "admin"
    private_key = file(var.private_key_location)
  }

  provisioner "file" {
    source = "payload/.env"
    destination = "/home/admin/.env"
  }

  provisioner "file" {
    source = "payload/install-git-on-debian-ec2.sh"
    destination = "/home/admin/install-git-on-debian-ec2.sh"
  }

  provisioner "remote-exec" {
    inline = [
        "sudo chmod u+x /home/admin/install-git-on-debian-ec2.sh",
        "/bin/bash /home/admin/install-git-on-debian-ec2.sh"
      ]
  }

  # local shell execution
  # provisioner "local-exec" {
  #   command = "echo ${self.public_ip} > output.txt"
  # }


  tags = {
    Name: "${var.env_prefix}-server"
  }
}
