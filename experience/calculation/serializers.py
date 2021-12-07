from rest_framework import serializers

from calculation.models import Candidate, Experience
from datetime import datetime


class ExperienceSerializer(serializers.ModelSerializer):

    start = serializers.CharField()
    end = serializers.CharField()

    class Meta:
        model = Experience
        fields = ['start', 'end']


class CandidateSerializer(serializers.ModelSerializer):

    workExperience = ExperienceSerializer(many=True, source='experiences')
    id = serializers.IntegerField(required=False)
    totalExperience = serializers.IntegerField(source='total_experience', required=False)
    name = serializers.CharField()

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'totalExperience', 'workExperience']

    def create(self, validated_data):
        experiences = validated_data.pop('experiences')
        candidate = Candidate.objects.create(**validated_data)
        for experience in experiences:
            Experience.objects.create(candidate=candidate, **experience)

        date_format = "%b %Y"
        work_experience = candidate.experiences.all().order_by('start')
        start_work = datetime.strptime(work_experience[0].start, date_format)
        end_work = datetime.strptime(work_experience[0].end, date_format)
        total = end_work - start_work
        print(total.days/30)

        for experience in work_experience[1:]:
            start_exp = datetime.strptime(experience.start, date_format)
            end_exp = datetime.strptime(experience.end, date_format)

            if start_exp < end_work:
                if end_exp > end_work:
                    total += end_exp - end_work

            if start_exp >= end_work:
                total += end_exp - start_exp

            if end_exp > end_work:
                end_work = end_exp

        total = total.days // 365
        candidate.total_experience = total
        candidate.save()

        return candidate
