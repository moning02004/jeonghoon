from rest_framework import serializers

from me.models import Career, Skill, CareerProject, Project, ProjectImage, CareerProjectImage


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        fields = kwargs.pop('fields', None)  # fields 인자 꺼내기
        exclude = kwargs.pop('exclude', None)
        self.model = model

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class CareerProjectImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = CareerProjectImage
        fields = ["url"]


class SkillSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class CareerProjectSerializer(serializers.ModelSerializer):
    images = CareerProjectImageSerializer(many=True, source="careerprojectimage_set")

    class Meta:
        model = CareerProject
        fields = ["title", "period", "content", "result", "images"]


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


class ProjectImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = ProjectImage
        fields = ["url"]

class ProjectDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(fields=["name"], many=True)
    images = ProjectImageSerializer(many=True, source="projectimage_set")

    class Meta:
        model = Project
        fields = ["title", "introduction", "content", "result", "skills", "images"]


class SkillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name", "description"]
