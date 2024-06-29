# Use a lighter base image with Python pre-installed
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential linux-libc-dev \
    wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion r-base mono-runtime libgomp1 libc6 curl grep sed dpkg tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
	bash ~/miniconda.sh -b -p /opt/conda && \
	rm ~/miniconda.sh

# Set environment variable
ENV PATH /opt/conda/bin:$PATH

# Fix for 'xgboost' missing
RUN conda install -y libgcc && \
    conda clean -a

# Set the working directory
WORKDIR /app

# Copy application files
COPY ./plaza /app/plaza

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/plaza/requirements.txt

# Use tini as the entrypoint
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python3"]
