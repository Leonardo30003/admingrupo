import reflex as rx
from .model.user_model import User
from .service.user_service import select_all_user_service,create_user_service

class UserState(rx.State):
    users: list[User] = []
    user_buscar: str = ""

    @rx.background
    async def get_all_users(self):
        async with self:
            self.users = select_all_user_service()

    
    @rx.background
    async def create_user(self, data: dict):
        async with self:
            try:
                self.users = create_user_service(data['username'],password=data['password'],phone=data['phone'],name=data['name'])
            except BaseException as be:
                print(be.args)

@rx.page(route='/user', title='user', on_load=UserState.get_all_users)
def user_page() -> rx.Component:
    return rx.flex(
        rx.heading('Usuarios', align='center'),
        rx.hstack(
            create_user_dialogo_component(),
            justify='center',
            style={'margin-top': '30px'}
        ),
        table_use(UserState.users),
        direction='column',
        style={"width": "60vw", "margin": "auto"}
    )

def table_use(list_user: list[User]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Nombre'),
                rx.table.column_header_cell('Email'),
                rx.table.column_header_cell('Telefono'),
                rx.table.column_header_cell('Accion'),
            )
        ),
        rx.table.body(
            rx.foreach(list_user, row_table)
        )
    )

def row_table(user: User) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.username),  
        rx.table.cell(user.phone),
        rx.table.cell(rx.hstack(
            rx.button('Eliminar')
        ))
    )







def create_user_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder='Nombre',
                name='name'
            ),
             rx.input(
                placeholder='Email',
                name='username'
            ),
             rx.input(
                placeholder='Contraseña',
                name='password',
                type='password'
            ),
             rx.input(
                placeholder='Telefono',
                name='phone'
            ),
            rx.dialog.close(
                rx.button('Guardar',type= 'submit')
            ),
        ),
        on_submit=UserState.create_user,
    )

def create_user_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear usuario")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear usuario"),
                create_user_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", color_scheme="gray", variant="soft")
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"width": "300px"},
        ),
    )
