from marshmallow import Schema, fields
from marshmallow.fields import Integer, String


class PlainStandardSchema(Schema):
    id: Integer = fields.Int(dump_only=True)
    name: String = fields.Str(required=True)


class UpdateStandardSchema(Schema):
    name: String = fields.Str(required=True)


class PlainSectionSchema(Schema):
    id: Integer = fields.Int(dump_only=True)
    name: String = fields.Str(required=True)


class UpdateSectionSchema(Schema):
    name: String = fields.Str(required=True)


class PlainSubjectSchema(Schema):
    id: Integer = fields.Int(dump_only=True)
    name: String = fields.Str(required=True)


class UpdateSubjectSchema(Schema):
    name: String = fields.Str()


class PlainTeacherSchema(Schema):
    id: Integer = fields.Int(dump_only=True)
    name: String = fields.Str(required=True)


class UpdateTeacherSchema(Schema):
    name: String = fields.Str()


class StandardSchema(PlainStandardSchema):
    sections = fields.List(fields.Nested(PlainSectionSchema(), dump_only=True))
    subjects = fields.List(fields.Nested(PlainSubjectSchema(), dump_only=True))


class SectionSchema(PlainSectionSchema):
    standards = fields.List(fields.Nested(PlainStandardSchema(), dump_only=True))


class SubjectSchema(PlainSectionSchema):
    standards = fields.List(fields.Nested(PlainStandardSchema(), dump_only=True))


class PlainClassRoomSchema(Schema):
    id = fields.Integer(dump_only=True)
    standard_id = fields.Integer(required=True, load_only=True)
    section_id = fields.Integer(required=True, load_only=True)
    teacher_id = fields.Integer(required=False, load_only=True)


class ClassRoomSchema(PlainClassRoomSchema):
    standard = fields.Nested(PlainStandardSchema())
    section = fields.Nested(PlainSectionSchema())
    teacher = fields.Nested(PlainTeacherSchema())


class ClassRoomSchemaWOTeacher(PlainClassRoomSchema):
    standard = fields.Nested(PlainStandardSchema())
    section = fields.Nested(PlainSectionSchema())


class PlainStandardSubjectSchema(Schema):
    id = fields.Integer(dump_only=True)
    standard_id = fields.Integer(required=True, load_only=True)
    subject_id = fields.Integer(required=True, load_only=True)


class StandardSubjectSchema(PlainStandardSubjectSchema):
    standard = fields.Nested(PlainStandardSchema())
    subject = fields.Nested(PlainSubjectSchema())


class PlainTeacherStandardSubjectSchema(Schema):
    id = fields.Integer(dump_only=True)
    teacher_id = fields.Integer(required=False, load_only=True)
    standard_subject_id = fields.Integer(required=True, load_only=True)


class TeacherStandardSubjectSchema(PlainTeacherStandardSubjectSchema):
    teacher = fields.Nested(PlainTeacherSchema())
    standard_subject = fields.Nested(StandardSubjectSchema())


class TeacherSchema(PlainTeacherSchema):
    class_rooms = fields.List(fields.Nested(ClassRoomSchemaWOTeacher(), dump_only=True))
    teacher_standard_subjects = fields.List(fields.Nested(TeacherStandardSubjectSchema(), dump_only=True))


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)
