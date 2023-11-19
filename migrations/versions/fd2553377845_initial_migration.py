"""Initial migration

Revision ID: fd2553377845
Revises: 
Create Date: 2023-10-07 13:36:31.214331

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fd2553377845'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('area',
    sa.Column('id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.Enum('GDE', 'COMPUTOS', 'SOPORTE', 'TELEFONIA', 'SISTEMAS', name='areaasignar'), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_modificacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_eliminacion', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='tickets'
    )
    op.create_table('tarea_area_relacion',
    sa.Column('id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), autoincrement=True, nullable=False),
    sa.Column('tarea', sa.String(length=256), nullable=False),
    sa.Column('area_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_modificacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_eliminacion', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['tickets.area.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='tickets'
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=256), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('apellido', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('celular', sa.String(length=256), nullable=True),
    sa.Column('telefono', sa.String(length=256), nullable=True),
    sa.Column('interno', sa.String(length=256), nullable=True),
    sa.Column('area_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=True),
    sa.Column('sede', sa.Enum('NUEVE_DE_JULIO', 'ANEXO1', 'ANEXO2', 'ANEXO3', name='esede'), nullable=False),
    sa.Column('piso', sa.String(length=256), nullable=True),
    sa.Column('perfil', sa.Enum('ADMINISTRADOR', 'TECNICO', 'ADMINISTRATIVO', 'SUPERADMIN', name='perfilusuario'), nullable=True),
    sa.Column('rol', sa.Enum('DIOS', 'ADMIN', 'EDITOR', 'LECTOR', name='rolusuario'), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_modificacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_eliminacion', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['tickets.area.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='tickets'
    )
    op.create_table('ticket',
    sa.Column('id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), autoincrement=True, nullable=False),
    sa.Column('identificador', sa.String(length=256), nullable=False),
    sa.Column('email_solicitante', sa.String(length=256), nullable=False),
    sa.Column('nombre_solicitante', sa.String(length=256), nullable=True),
    sa.Column('telefono_solicitante', sa.String(length=256), nullable=True),
    sa.Column('celular_solicitante', sa.String(length=256), nullable=True),
    sa.Column('area_solicitante', sa.Enum('ADMINISTRACION', 'RRHH', 'CONTABILIDAD', 'LEGALES', name='areassolicitante'), nullable=False),
    sa.Column('sede_solicitante', sa.Enum('NUEVE_DE_JULIO', 'ANEXO1', 'ANEXO2', 'ANEXO3', name='esede'), nullable=False),
    sa.Column('piso_solicitante', sa.String(length=256), nullable=True),
    sa.Column('referencia', sa.String(length=256), nullable=True),
    sa.Column('area_asignada_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=False),
    sa.Column('tecnico_asignado_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=True),
    sa.Column('prioridad', sa.Enum('ALTA', 'BAJA', name='prioridadticket'), nullable=False),
    sa.Column('estado', sa.Enum('PENDIENTE', 'EN_CURSO', 'FINALIZADO', 'DERIVADO', 'ANULADO', name='estadoticket'), nullable=False),
    sa.Column('descripcion', sa.Text(length=1048576), nullable=True),
    sa.Column('pre_tarea', sa.Enum('TAREA1', 'TAREA2', 'TAREA3', name='epretareas'), nullable=True),
    sa.Column('archivos', sa.String(length=256), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_modificacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_eliminacion', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['area_asignada_id'], ['tickets.area.id'], ),
    sa.ForeignKeyConstraint(['tecnico_asignado_id'], ['tickets.usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('identificador'),
    schema='tickets'
    )
    op.create_table('ticket_historial',
    sa.Column('id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), autoincrement=True, nullable=False),
    sa.Column('ticket_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=False),
    sa.Column('registro_anterior_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=True),
    sa.Column('area_anterior_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=True),
    sa.Column('tecnico_anterior_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=True),
    sa.Column('notas', sa.Text(length=1048576), nullable=True),
    sa.Column('creado_por_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_modificacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['area_anterior_id'], ['tickets.area.id'], ),
    sa.ForeignKeyConstraint(['creado_por_id'], ['tickets.usuario.id'], ),
    sa.ForeignKeyConstraint(['registro_anterior_id'], ['tickets.ticket_historial.id'], ),
    sa.ForeignKeyConstraint(['tecnico_anterior_id'], ['tickets.usuario.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.ticket.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='tickets'
    )
    op.create_table('ticket_tarea_relacion',
    sa.Column('id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), autoincrement=True, nullable=False),
    sa.Column('ticket_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=False),
    sa.Column('tarea_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=False),
    sa.Column('tecnico_id', sa.Integer().with_variant(mysql.INTEGER(unsigned=True), 'mysql'), nullable=False),
    sa.Column('estado', sa.Enum('ACTIVA', 'FINALIZADA', name='eestadotarea'), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_modificacion', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('fecha_eliminacion', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tarea_id'], ['tickets.tarea_area_relacion.id'], ),
    sa.ForeignKeyConstraint(['tecnico_id'], ['tickets.usuario.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.ticket.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='tickets'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket_tarea_relacion', schema='tickets')
    op.drop_table('ticket_historial', schema='tickets')
    op.drop_table('ticket', schema='tickets')
    op.drop_table('usuario', schema='tickets')
    op.drop_table('tarea_area_relacion', schema='tickets')
    op.drop_table('area', schema='tickets')
    # ### end Alembic commands ###
