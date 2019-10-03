FROM considerate/nak-learn:music

RUN pip3 --no-cache-dir install \
    backtrader

WORKDIR /code
VOLUME ["/data", "/models", "/notebooks"]

# Expose Jupyter port
EXPOSE 8888
CMD jupyter notebook --notebook-dir=.
