from odufrn_downloader import ODUFRNDownloader


ufrn_data = ODUFRNDownloader()
datasets = [
    'discentes',
    'bolsas-de-apoio',
    'bolsistas-de-iniciacao-cientifica',
]

# Download
for dataset in datasets:
    ufrn_data.download_package(dataset, 'data/')
