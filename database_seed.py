from api.adapters.outbound.database.models.user import User
from api.adapters.outbound.database.models.group import Group
from api.adapters.outbound.database.models.robot import Robot


def populate_database():
    user = User.objects.create(
        name="Test man",
        email="example@example.com",
        password="12345",
    )
    print("User created", user)

    group_a = Group.objects.create(
        name="Grupo A", description="Este eh um grupo de testes"
    )
    group_b = Group.objects.create(
        name="Grupo B", description="Este eh um grupo de testes"
    )
    group_c = Group.objects.create(
        name="Grupo C", description="Este eh um grupo de testes"
    )
    print("Group created", group_a)
    print("Group created", group_b)
    print("Group created", group_c)

    user.groups.add(group_a)
    user.groups.add(group_b)
    user.groups.add(group_c)
    user.save()

    robot_a = Robot.objects.create(
        name="Bot Mock",
        description="Inserir usuarios no django admin",
        group=group_a,
        section_name="section1",
    )
    robot_b = Robot.objects.create(
        name="Bot Ping",
        description="Acessar uma URL qualquer",
        group=group_b,
        section_name="section2",
    )
    robot_c = Robot.objects.create(
        name="Bot Sipec",
        description="Preencher formulario na plataforma SIPEC",
        group=group_c,
        section_name="section3",
    )
    print("Robot created", robot_a)
    print("Robot created", robot_b)
    print("Robot created", robot_c)


populate_database()
