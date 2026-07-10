FROM continuumio/miniconda3:22.11.1

COPY environment.yml .
RUN conda env create -f environment.yml

RUN echo "conda activate assignment5env" >> ~/.bashrc
ENV PATH="$PATH:/opt/conda/envs/assignment5env/bin"

RUN useradd -m assign5user
USER assign5user

WORKDIR /home/assign5user

# Expose the JupyterLab port
EXPOSE 8888

# Start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0"]
