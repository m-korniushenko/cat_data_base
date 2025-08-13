from datetime import datetime, timedelta

import pandas as pd
from database_folder.models import (ClubMember, Clubs, Events, Registrations,
                                    Users, VisitHistory, Lessons, VisitClub)
from database_folder.postgres import async_engine, async_session
from dateutil.relativedelta import relativedelta
from sqlalchemy import (BigInteger, MetaData, Table, and_, asc, cast, delete,
                        desc, text, update, func)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from system_staff.logger import log_function_call, logger


class AsyncOrm:
    @log_function_call
    @staticmethod
    async def postgres_get_users(user_id: int = None, category=None,
                                 permission=None, user_confrimrulls=None):
        async with async_session() as session:
            if category:
                result = await session.execute(
                    select(Users).filter_by(user_status=category)
                )
                return result.scalars().all()
            if user_id:
                user_id = int(user_id)
                query = select(Users).filter_by(user_id=int(user_id))
                result = await session.execute(query)
                return result.scalars().first()
            query = select(Users)
            if permission is not None:
                query = query.filter(Users.user_permission == permission)
            if user_confrimrulls is not None:
                query = query.filter(
                    Users.user_confrimrulls == user_confrimrulls)
            query = query.order_by(Users.user_firstname)
            result = await session.execute(query)
            return result.scalars().all()

    @log_function_call
    @staticmethod
    async def get_unregistered_users(event_id, status):
        falg = True
        event_id = int(event_id)
        async with async_session() as session:
            UserAlias = aliased(Users)
            RegistrationAlias = aliased(Registrations)
            query = (
                select(UserAlias)
                .outerjoin(
                    RegistrationAlias,
                    (UserAlias.user_id == RegistrationAlias.user_id) &
                    (RegistrationAlias.event_id == event_id)
                )
                .where(RegistrationAlias.user_id.is_(None)))
            if status == "iceberg":
                query = query.where(UserAlias.user_status == "iceberg")
            query = query.where(UserAlias.user_permission == falg)
            result = await session.execute(query)
            return result.scalars().all()

    @log_function_call
    @staticmethod
    async def postgres_delete_user(user_id):
        if user_id:
            user_id = int(user_id)
        async with async_session() as session:
            result = await session.execute(select(Users
                                                  ).filter_by(user_id=user_id))
            user = result.scalar()
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False

    @log_function_call
    @staticmethod
    async def postgres_get_events(event_id: int = None, future: bool = True,
                                  status=None, limit=None):
        async with async_session() as session:
            if event_id:
                event_id = int(event_id)
                result = await session.execute(
                    select(Events).filter_by(event_id=int(event_id))
                )
                event = result.scalars().first()
                return event
            datetime_now = datetime.now()
            query = select(Events)
            if future:
                two_hours_ago = datetime_now - timedelta(hours=2)
                query = query.filter(Events.event_datetime >= two_hours_ago)
                if status == "ordinary":
                    query = query.filter_by(event_type="ordinary")
            else:
                query = query.filter(Events.event_datetime <= datetime_now)
                if limit:
                    query = query.limit(limit)
            query = query.order_by(asc(Events.event_datetime))
            result = await session.execute(query)
            events = result.scalars().all()
            return events

    @log_function_call
    @staticmethod
    async def postgree_update_registration(user_id, event_id, status):
        async with async_session() as session:
            query = select(Registrations).filter_by(
                user_id=user_id).filter_by(event_id=event_id)
            result = await session.execute(query)
            registration = result.scalars().first()
            registration.status = status
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_edit_event(event_id: int, table: str, new_info):
        event_id = int(event_id)
        async with async_session() as session:
            query = select(Events).filter_by(event_id=event_id)
            result = await session.execute(query)
            event = result.scalars().first()
            setattr(event, table, new_info)
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_get_registrations(user_id: int = None,
                                         event_id: int = None,
                                         future=False,
                                         status=None):
        if user_id:
            user_id = int(user_id)
        if event_id:
            event_id = int(event_id)

        async with async_session() as session:
            query = select(Users, Registrations, Events).join(
                Registrations, Users.user_id == Registrations.user_id).join(
                Events, Registrations.event_id == Events.event_id)
            filters = []
            if status:
                filters.append(Registrations.status == status)
            if user_id:
                filters.append(Registrations.user_id == user_id)
            if event_id:
                filters.append(Registrations.event_id == event_id)
            if future and user_id:
                filters.append(Events.event_datetime > datetime.now())
            if filters:
                query = query.filter(*filters)
            if future:
                query = query.order_by(asc(Events.event_datetime))

            result = await session.execute(query)
            if user_id and event_id:
                return result.first()
            else:
                return result.all()

    @log_function_call
    @staticmethod
    async def postgres_get_users_registrations(event_id: int, reg_status: str):
        async with async_session() as session:
            query = select(Users, Registrations, Events).join(
                Registrations, Users.user_id == Registrations.user_id).join(
                    Events, Events.event_id == Registrations.event_id
                    ).filter(Registrations.status == reg_status,
                             Registrations.event_id == event_id)
            result = await session.execute(query)
            registrations = result.all()
            return registrations

    @log_function_call
    @staticmethod
    async def postgres_insert_user(user_id: int, user_nickname: str,
                                   file_path: str, kyc_doc_type: bool = False,
                                   user_status='ordinary'):
        async with async_session() as session:
            new_user = Users(
                user_id=user_id,
                user_nickname=user_nickname,
                user_photopath=file_path,
                kyc_choice=kyc_doc_type,
                user_status=user_status)
        session.add(new_user)
        await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_update_user(user_id: int,
                                   user_firstname=None,
                                   user_surname=None,
                                   user_birthday=None,
                                   user_mail=None,
                                   user_status=None,
                                   user_permission=None,
                                   user_photopath=None,
                                   user_lang=None):
        user_id = int(user_id)
        async with async_session() as session:
            query = select(Users).filter_by(user_id=user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if user_firstname:
                user.user_firstname = user_firstname
            if user_surname:
                user.user_surname = user_surname
            if user_mail:
                user.user_mail = user_mail
            if user_birthday:
                user.user_birthday = datetime.strptime(
                    user_birthday, '%d-%m-%Y')
            if user_status:
                user.user_status = user_status
            if user_permission is not None:
                user.user_permission = user_permission
            if user_photopath:
                user.user_photopath = user_photopath
            if user_lang:
                user.user_lang = user_lang
            await session.commit()
        return user

    @log_function_call
    @staticmethod
    async def postgres_insert_registration(user_id: int, event_id: int
                                           ) -> bool:
        if user_id:
            user_id = int(user_id)
        if event_id:
            event_id = int(event_id)
        async with async_session() as session:
            new_registration = Registrations(
                user_id=user_id, event_id=event_id)
            session.add(new_registration)
            try:
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                logger.error(f"""Registration already exists for user_id:
                      {user_id} and event_id: {event_id}""")
                return False

    @log_function_call
    @staticmethod
    async def postgres_delete_registration(event_id=None, user_id=None):
        if event_id:
            event_id = int(event_id)
        if user_id:
            user_id = int(user_id)
        async with async_session() as session:
            query = delete(Registrations)
            if user_id and event_id:
                query = query.filter_by(
                    user_id=user_id, event_id=event_id)
            elif user_id:
                query = query.filter_by(user_id=user_id)
            elif event_id:
                query = query.filter_by(event_id=event_id)
            await session.execute(query)
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_insert_event(events_info, file_hash_name):
        async with async_session() as session:
            new_event = Events(
                event_id=file_hash_name,
                event_name=events_info['event-add-name'],
                event_datetime=datetime.strptime(
                    events_info['event-add-datetime'], '%Y-%m-%d %H:%M'),
                event_registration_deadline=datetime.strptime(
                    events_info['event-add-datetime'], '%Y-%m-%d %H:%M'),
                event_description=events_info['event-add-description'],
                event_picture_path=events_info['event-add-picture-path'],
                event_max_registration=100
            )
            session.add(new_event)
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_delete_event(event_id: int):
        if event_id:
            event_id = int(event_id)
        async with async_session() as session:
            query = select(Events).filter_by(event_id=event_id)
            result = await session.execute(query)
            event = result.scalars().first()
            if event:
                await session.delete(event)
                await session.commit()
                return True
            return False

    @log_function_call
    @staticmethod
    async def delete_table(table_name: str):
        metadata = MetaData()
        try:
            await metadata.reflect(bind=async_engine)
            registrations_table = Table(table_name, metadata)
            await registrations_table.drop(async_engine)
            print("Таблица удалена")
        except SQLAlchemyError as ex:
            print(f"Ошибка: {ex}")

    @log_function_call
    @staticmethod
    async def postgres_get_events_period(start, end):
        async with async_session() as session:
            query = select(Events).filter(
                Events.event_datetime >= start,
                Events.event_datetime <= end
            ).order_by(asc(Events.event_datetime))
            result = await session.execute(query)
            events_this_week = result.scalars().all()
            return events_this_week

    @log_function_call
    @staticmethod
    async def postgres_users_by_registrations(event_id, registered=False):
        event_id = int(event_id)
        async with async_session() as session:
            query = select(Users).join(
                Registrations, Users.user_id == Registrations.user_id
            ).filter(
                Registrations.event_id == event_id,
                Registrations.status == registered
            ).order_by(Users.user_firstname)
            result = await session.execute(query)
            registrations = result.scalars().all()
            return registrations

    @log_function_call
    @staticmethod
    async def postgres_edit_user(user_id, table, new_info):
        user_id = int(user_id)
        async with async_session() as session:
            result = await session.execute(select(Users).filter_by(
                user_id=user_id))
            user = result.scalar_one_or_none()
            if user:
                setattr(user, table, new_info)
                await session.commit()
                return True
            else:
                return False

    @log_function_call
    @staticmethod
    async def postgres_shufa(user_id, count, plus=None):
        async with async_session() as session:
            result = await session.execute(select(Users).filter_by(
                user_id=user_id))
            user = result.scalars().first()
            if not user:
                return None
            if plus is True:
                user.user_shufa += count
            elif plus is False:
                user.user_shufa -= count
            elif plus is None:
                shufa = user.user_shufa
                await session.commit()
                return shufa
            shufa = user.user_shufa
            await session.commit()
            return shufa

    @log_function_call
    @staticmethod
    async def postgres_record_visit(user_id: int, visit_schufa: int,
                                    visit_cause: str, visit_param: str):
        async with async_session() as session:
            visit = VisitHistory(
                user_id=user_id, visit_cause=visit_cause,
                visit_schufa=visit_schufa, visit_param=str(visit_param))
            session.add(visit)
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_get_last_visit(user_id, visit_cause):
        async with async_session() as session:
            query = select(VisitHistory).filter_by(
                user_id=user_id).filter_by(
                    visit_cause=visit_cause).order_by(
                        desc(VisitHistory.visit_datetime))
            result = await session.execute(query)
            last_visit = result.scalars().first()
            return last_visit

    @log_function_call
    @staticmethod
    async def postgres_get_last_visit_param(user_id, visit_param):
        async with async_session() as session:
            result = await session.execute(
                select(VisitHistory).filter_by(
                    user_id=user_id,
                    visit_param=str(visit_param)
                ).order_by(desc(VisitHistory.visit_datetime))
            )
            last_visit = result.scalars().first()
            return last_visit

    @log_function_call
    @staticmethod
    def format_dates(df, date_columns):
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M')
        return df

    @log_function_call
    @staticmethod
    def adjust_column_widths(worksheet):
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            adjusted_width = max_length + 2
            worksheet.column_dimensions[
                column[0].column_letter].width = adjusted_width

    @log_function_call
    @staticmethod
    def export_to_excel(data, output_file, date_columns):
        df = pd.DataFrame(data)
        if df.empty:
            logger.warning("No data to write to Excel.")
            return
        df = AsyncOrm.format_dates(df, date_columns)
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            worksheet = writer.sheets['Sheet1']
            AsyncOrm.adjust_column_widths(worksheet)

    @log_function_call
    @staticmethod
    async def postgres_visit_history_full():
        output_file = 'visit_history_full.xlsx'
        end = datetime.now()
        start = datetime.now() - relativedelta(months=6)

        async with async_session() as session:
            result = await session.execute(
                select(
                    VisitHistory.visit_datetime,
                    VisitHistory.visit_cause,
                    VisitHistory.visit_param,
                    Users.user_id,
                    Users.user_nickname,
                    Users.user_firstname,
                    Users.user_surname,
                    Users.user_birthday,
                    VisitHistory.visit_schufa
                ).join(
                    Users, VisitHistory.user_id == Users.user_id
                ).filter(
                    and_(
                        VisitHistory.visit_datetime >= start,
                        VisitHistory.visit_datetime <= end
                    )
                ).order_by(VisitHistory.visit_datetime)
            )
            visit_history = result.fetchall()
            if not visit_history:
                logger.warning("No data available for the given date range.")
                return None
            AsyncOrm.export_to_excel(visit_history, output_file,
                                     ['user_birthday', 'visit_datetime'])
        return output_file

    @log_function_call
    @staticmethod
    async def postgres_visit_history_local(param, event_club_id=None):
        output_file = f'visit_history_{param}.xlsx'
        end = datetime.now()
        start = datetime.now() - relativedelta(months=6)

        async with async_session() as session:
            if param == "rg":
                query = select(
                    VisitHistory.visit_datetime,
                    Events.event_name,
                    Users.user_id,
                    Users.user_nickname,
                    Users.user_firstname,
                    Users.user_surname,
                    Users.user_birthday,
                    VisitHistory.visit_schufa
                ).filter(VisitHistory.visit_cause == param).join(
                    Users, VisitHistory.user_id == Users.user_id
                ).join(
                    Events, Events.event_id == cast(
                        VisitHistory.visit_param, BigInteger)
                )
            elif param == "clubchin":
                query = select(
                    VisitHistory.visit_datetime,
                    Clubs.club_name,
                    Users.user_id,
                    Users.user_nickname,
                    Users.user_firstname,
                    Users.user_surname,
                    Users.user_birthday,
                    VisitHistory.visit_schufa
                ).filter(VisitHistory.visit_cause == param).join(
                    Users, VisitHistory.user_id == Users.user_id
                ).join(
                    Clubs, Clubs.club_id == cast(
                        VisitHistory.visit_param, BigInteger)
                )

            query = query.filter(
                and_(
                    VisitHistory.visit_datetime >= start,
                    VisitHistory.visit_datetime <= end
                )
            ).order_by(VisitHistory.visit_datetime)

            if event_club_id:
                query = query.filter(VisitHistory.visit_param == event_club_id)

            result = await session.execute(query)
            visit_history = result.all()

            AsyncOrm.export_to_excel(
                visit_history, output_file, ['user_birthday', 'visit_datetime']
            )

        return output_file

    @log_function_call
    @staticmethod
    async def postgres_add_club(club_name, club_description, club_max_seats
                                ) -> Clubs:
        club_max_seats = int(club_max_seats)
        async with async_session() as session:
            club = Clubs(club_name=club_name,
                         club_description=club_description,
                         club_max_seats=club_max_seats)
            session.add(club)
            await session.commit()
            result = await session.execute(select(Clubs).filter_by(
                club_name=club_name))
            return result.scalar_one()

    @log_function_call
    @staticmethod
    async def postgres_get_clubs(club_id=None, teacher_id=None):
        if club_id:
            club_id = int(club_id)
        if teacher_id:
            teacher_id = int(teacher_id)
        async with async_session() as session:
            if club_id:
                result = await session.execute(select(Clubs).filter_by(
                    club_id=club_id))
                return result.scalar_one_or_none()
            elif teacher_id:
                result = await session.execute(select(Clubs).filter_by(
                    club_teacher_id=teacher_id))
                return result.scalars().all()
            else:
                result = await session.execute(select(Clubs))
                return result.scalars().all()

    @log_function_call
    @staticmethod
    async def postgres_remove_club_member(user_id=None, club_id=None):
        if club_id is None:
            raise ValueError("Необходимо указать club_id")
        if user_id:
            user_id = int(user_id)
        club_id = int(club_id)
        async with async_session() as session:
            if user_id:
                query = delete(ClubMember).where(
                    ClubMember.user_id == user_id,
                    ClubMember.club_id == club_id)
            else:
                query = delete(ClubMember).where(
                    ClubMember.club_id == club_id)
            await session.execute(query)
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_del_club(club_id):
        club_id = int(club_id)
        async with async_session() as session:
            club = await session.get(Clubs, club_id)
            if club:
                await session.delete(club)
                await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_add_club_member(user_id: int, club_id: int):
        user_id, club_id = int(user_id), int(club_id)
        async with async_session() as session:
            new_member = ClubMember(
                user_id=user_id,
                club_id=club_id)
            session.add(new_member)
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_del_club_member(user_id=None, club_id=None):
        if user_id:
            user_id = int(user_id)
        if club_id:
            club_id = int(club_id)
        async with async_session() as session:
            query = delete(ClubMember)
            if user_id and club_id:
                query = query.filter_by(
                    user_id=user_id, club_id=club_id)
            elif user_id:
                query = query.filter_by(user_id=user_id)
            elif club_id:
                query = query.filter_by(club_id=club_id)
            await session.execute(query)
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_get_clubs_member(user_id=None, club_id=None,
                                        status=None):
        if club_id:
            club_id = int(club_id)
        if user_id:
            user_id = int(user_id)
        async with async_session() as session:
            query = select(Clubs, Users, ClubMember).join(
                ClubMember, Clubs.club_id == ClubMember.club_id).join(
                Users, ClubMember.user_id == Users.user_id
            )
            if user_id and club_id and status:
                result = await session.execute(
                    query.filter(
                        Users.user_id == user_id,
                        Clubs.club_id == club_id,
                        ClubMember.club_user_status == status
                    )
                )
                return result.first()
            elif user_id and club_id:
                result = await session.execute(
                    query.filter(
                        ClubMember.user_id == user_id,
                        Clubs.club_id == club_id
                    )
                )
                return result.first()
            elif user_id:
                result = await session.execute(
                    query.filter(Users.user_id == user_id)
                )
                return result.all()
            elif status and club_id:
                result = await session.execute(
                    query.filter(
                        ClubMember.club_user_status == status,
                        Clubs.club_id == club_id))
                return result.all()
            elif status:
                result = await session.execute(
                    query.filter(ClubMember.club_user_status == status)
                )
                return result.all()
            elif club_id:
                result = await session.execute(
                    query.filter(Clubs.club_id == club_id)
                )
                return result.scalars().all()
            result = await session.execute(query)
            return result.scalars().all()

    @log_function_call
    @staticmethod
    async def postgres_update_member_user(user_id, club_id, new_status):
        if user_id:
            user_id = int(user_id)
        if club_id:
            club_id = int(club_id)
        async with async_session() as session:
            result = await session.execute(
                select(ClubMember).filter_by(
                    user_id=user_id,
                    club_id=club_id
                )
            )
            member = result.scalar_one_or_none()
            if member:
                member.club_user_status = new_status
                await session.commit()
            else:
                raise ValueError(
                    "No member found with the given user_id and club_id")

    @log_function_call
    @staticmethod
    async def add_new_column():
        comm = "ALTER TABLE users ADD COLUMN user_lang VARCHAR(2) DEFAULT 'RU'"
        async with async_session() as session:
            await session.execute(text(comm))
            await session.commit()

    @log_function_call
    @staticmethod
    async def postgres_edit_club(
         club_id: int, table: str, new_info: str | int):
        async with async_session() as session:
            query = select(Clubs).where(Clubs.club_id == int(club_id))
            result = await session.execute(query)
            club = result.scalar_one()
            if club:
                setattr(club, table, new_info)
                await session.commit()
            else:
                raise ValueError("Club not found")

    @log_function_call
    @staticmethod
    async def get_lessons(club_id: int = None,
                          teacher_id: int = None,
                          lesson_id: int = None,
                          target_date: datetime = None):
        club_id = int(club_id) if club_id else None
        teacher_id = int(teacher_id) if teacher_id else None
        lesson_id = int(lesson_id) if lesson_id else None
        query = select(Lessons)
        if club_id:
            query = query.where(Lessons.club_id == club_id)
        if teacher_id:
            query = query.where(Lessons.teacher_id == teacher_id)
        if lesson_id:
            query = query.where(Lessons.lesson_id == lesson_id)
        if target_date:
            query = query.where(func.date(
                Lessons.lesson_datetime) == target_date)
        async with async_session() as session:
            result = await session.execute(query)
        if lesson_id:
            return result.scalar_one_or_none()
        return result.scalars().all()

    @log_function_call
    @staticmethod
    async def create_lesson(club_id: int = None,
                            teacher_id: int = None):
        club_id = int(club_id) if club_id else None
        teacher_id = int(teacher_id) if teacher_id else None
        lesson = Lessons(club_id=club_id, teacher_id=teacher_id)
        async with async_session() as session:
            async with session.begin():
                session.add(lesson)
                await session.flush()
                await session.refresh(lesson)
                return lesson.lesson_id

    @log_function_call
    @staticmethod
    async def edit_lesson(lesson_id: int, table: str, new_info: str):
        lesson_id = int(lesson_id)
        query = (
            update(Lessons).where(
                Lessons.lesson_id == lesson_id).values({table: new_info}))
        async with async_session() as session:
            await session.execute(query)
            await session.commit()
            return True

    @log_function_call
    @staticmethod
    async def insert_visit_to_club(club_id: int, lesson_id: int, user_id: int):
        club_id, lesson_id, user_id = int(
            club_id), int(lesson_id), int(user_id)
        visit = VisitClub(
            club_id=club_id, lesson_id=lesson_id, user_id=user_id)
        async with async_session() as session:
            async with session.begin():
                session.add(visit)
                await session.flush()
                await session.refresh(visit)
                return visit.visit_id

    @log_function_call
    @staticmethod
    async def get_visit_club(club_id: int, lesson_id: int,
                             target_date: datetime, user_id: int):
        club_id = int(club_id) if club_id else None
        lesson_id = int(lesson_id) if lesson_id else None
        user_id = int(user_id) if user_id else None
        query = select(VisitClub)
        if club_id:
            query = query.where(VisitClub.club_id == club_id)
        if lesson_id:
            query = query.where(VisitClub.lesson_id == lesson_id)
        if target_date:
            query = query.where(func.date(
                VisitClub.visit_datetime) == target_date)
        if user_id:
            query = query.where(VisitClub.user_id == user_id)
        async with async_session() as session:
            result = await session.execute(query)
        if lesson_id:
            return result.first()
        return result.scalars().all()

    @log_function_call
    @staticmethod
    async def get_visit_club_member(club_id: int, lesson_id: int):
        club_id = int(club_id) if club_id else None
        lesson_id = int(lesson_id) if lesson_id else None
        query = (
            select(Clubs, Users, ClubMember)
            .join(VisitClub, VisitClub.club_id == Clubs.club_id)
            .join(Users, VisitClub.user_id == Users.user_id)
            .join(ClubMember, ClubMember.user_id == Users.user_id))
        if club_id:
            query = query.where(VisitClub.club_id == club_id)
        if lesson_id:
            query = query.where(VisitClub.lesson_id == lesson_id)
        async with async_session() as session:
            result = await session.execute(query)
            return result.all()

    @log_function_call
    @staticmethod
    async def execute_script(query: str):
        query = text(query)
        async with async_session() as session:
            await session.execute(query)
            await session.commit()
