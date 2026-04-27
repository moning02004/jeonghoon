from rest_framework import serializers

from me.models import Career, Skill, CareerProject, Project


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # fields 인자 꺼내기
        exclude = kwargs.pop('exclude', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class SkillSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class CareerProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProject
        fields = ["title", "period", "content", "result"]


class CareerDetailSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()
    skills = SkillSerializer(fields=["name"], many=True)
    projects = CareerProjectSerializer(many=True, source="careerproject_set")

    class Meta:
        model = Career
        fields = ["company", "position", "period", "introduction", "summary", "skills", "projects"]

    @staticmethod
    def get_period(obj):
        end = obj.end_date or "현재"
        return f"{obj.start_date} - {end}"


class ProjectDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(fields=["name"], many=True)

    class Meta:
        model = Project
        fields = ["title", "introduction", "content", "result", "skills"]


class SkillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name", "description"]
