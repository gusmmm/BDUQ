from datetime import date, datetime

from sqlalchemy import Date, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass()
class Doente:
    __tablename__ = 'doentes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    numero_processo: Mapped[int] = mapped_column(unique=True)
    nome: Mapped[str]
    data_nascimento: Mapped[date] = mapped_column(Date())  # was str
    sexo: Mapped[str]
    morada: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False,
                                                 server_default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        init=False,
        default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
