FROM python:3.10

COPY ./ /app
WORKDIR /app/
ENV PYTHONPATH=/app

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then python -m pip install \".[tests]\" ; else python -m pip install . ; fi"

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./start_reload.sh /start_reload.sh
RUN chmod +x /start-reload.sh

EXPOSE 80

CMD ["/start.sh"]