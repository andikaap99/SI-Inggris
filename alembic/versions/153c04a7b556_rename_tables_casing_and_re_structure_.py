"""rename tables casing and re-structure category tables

Revision ID: 153c04a7b556
Revises: 348d790f1229
Create Date: 2025-07-20 11:29:26.349135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '153c04a7b556'
down_revision: Union[str, Sequence[str], None] = '348d790f1229'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "Category",
        sa.Column("Id_cat", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50)),
    )

    # Rename tabel agar sesuai dengan casing di model Python
    op.rename_table("image_word", "Image_Word")
    op.rename_table("attempt_image_word", "Attempt_Image_Word")

    # Drop foreign key constraint dari Image_Word ke Category_Image_Word
    op.drop_constraint("image_word_ibfk_1", "Image_Word", type_="foreignkey")

    # Rename kolom Id_ciw menjadi Id_cat
    op.alter_column("Image_Word", "Id_ciw", new_column_name="Id_cat", existing_type=sa.Integer)

    # Tambahkan foreign key baru ke tabel Category
    op.create_foreign_key(
        "fk_image_word_category",  # nama constraint baru
        "Category",              # tabel sumber
        "Image_Word",                # tabel tujuan
        ["Id_cat"],                # kolom di sumber
        ["Id_cat"]                 # kolom di tujuan
    )

    # Drop tabel Category_Image_Word karena tidak digunakan lagi
    op.drop_table("category_image_word")


def downgrade():
    # Buat ulang tabel Category_Image_Word (hanya contoh minimal)
    op.create_table(
        "category_image_word",
        sa.Column("Id_ciw", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50)),
    )

    # Hapus FK baru
    op.drop_constraint("fk_image_word_category", "Image_Word", type_="foreignkey")

    # Rename kolom kembali
    op.alter_column("Image_Word", "Id_cat", new_column_name="Id_ciw")

    # Tambahkan kembali FK lama
    op.create_foreign_key(
        "image_word_ibfk_1",
        "Image_Word",
        "category_image_word",
        ["Id_ciw"],
        ["Id_ciw"]
    )

    # Rename tabel kembali ke nama awal
    op.rename_table("Image_Word", "image_word")
    op.rename_table("Attempt_Image_Word", "attempt_image_word")
