from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Consumer
from .serializers import GeoJSONSerializer


class ConsumerView(APIView):
    def get(self, request):
        min_previous_jobs_count = request.GET.get('min_previous_jobs_count')
        max_previous_jobs_count = request.GET.get('max_previous_jobs_count')
        previous_jobs_count = request.GET.get('previous_jobs_count')
        status = request.GET.get('status')

        # Filter consumers based on query parameters
        consumers = Consumer.objects.all()
        if min_previous_jobs_count:
            consumers = consumers.filter(previous_jobs_count__gte=min_previous_jobs_count)
        if max_previous_jobs_count:
            consumers = consumers.filter(previous_jobs_count__lte=max_previous_jobs_count)
        if previous_jobs_count:
            consumers = consumers.filter(previous_jobs_count=previous_jobs_count)
        if status:
            consumers = consumers.filter(status=status)

        # Paginate results
        paginator = Paginator(consumers, 10)  # Show 10 consumers per page
        page = request.GET.get('page')
        try:
            consumers_page = paginator.page(page)
        except PageNotAnInteger:
            consumers_page = paginator.page(1)
        except EmptyPage:
            consumers_page = paginator.page(paginator.num_pages)

        # Serialize to GeoJSON
        serializer = GeoJSONSerializer({'features': consumers_page})
        geojson = serializer.data

        # Build response with paging links
        links = []
        if consumers_page.has_previous():
            links.append('<{}>; rel="prev"'.format(request.path + '?page=' + str(consumers_page.previous_page_number())))
        if consumers_page.has_next():
            links.append('<{}>; rel="next"'.format(request.path + '?page=' + str(consumers_page.next_page_number())))
        response = Response(geojson)
        if links:
            response['Link'] = ', '.join(links)
        return response
