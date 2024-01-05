FROM python:3.10-slim

# Install miniconda 
RUN apt-get update \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh\
    && bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 \
    && rm -rf ~/miniconda3/miniconda.sh 

# Add Conda executable to PATH
ENV PATH=~/miniconda3/bin:$PATH

# Set the working directory to /app
WORKDIR /app

# Copy required contents into the container at /app
COPY configure /app/configure
COPY src /app/src
COPY run.sh /app/run.sh
COPY venv.yaml /app/venv.yaml

RUN chmod +x run.sh
# Create the environment and install requirements
# RUN pip install -r requirements.txt
RUN ~/miniconda3/bin/conda env create -f venv.yaml
SHELL ["/bin/bash", "-c"]
# RUN ~/miniconda3/bin/conda init bash
# RUN ~/miniconda3/bin/conda activate nlp-tunnel-vision
# Activate the Conda environment
# Activate the Conda environment
RUN echo "source activate nlp-tunnel-vision" > ~/.bashrc
ENV PATH ~/miniconda3/envs/nlp-tunnel-vision/bin:$PATH
RUN /bin/bash -c "source activate nlp-tunnel-vision"


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
ENTRYPOINT ["/bin/bash", "/app/run.sh"]
