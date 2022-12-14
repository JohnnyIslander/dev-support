from os.path import split

from witness import Batch
from witness.providers.pandas.extractors import PandasExcelExtractor
from external.utils.var import color


def _handle_multi_sheet(output):
    dfs = []
    for sheet_name, frame in output.items():
        frame['sheet_name'] = sheet_name
        dfs.append(frame)
    return dfs


def _extract_and_normalize(extractor, config, transformation=None):
    from pandas import concat
    extractor.extract()
    raw_output = extractor.output

    dfs = _handle_multi_sheet(raw_output) if extractor.sheet_name is None \
        else [raw_output]

    transformed_dfs = []

    for df in dfs:
        df.dropna(axis=1, inplace=True, how='all')
        if transformation is not None:
            transformed_df = transformation(df, config)
            transformed_dfs.append(transformed_df)
        else:
            transformed_dfs = dfs

    united_df = concat(transformed_dfs)

    setattr(extractor, 'output', united_df)

    extractor.unify()

    return extractor.output


def extract(uri, config, dump_dir=None, transformation=None):

    src_cfg = config['extract']['src']
    if transformation is not None:
        tsf_config = config['transform']
    else:
        tsf_config = None
    src_cfg['uri'] = uri

    extractor = PandasExcelExtractor(**src_cfg, dtype='string',)

    output = _extract_and_normalize(extractor, config=tsf_config, transformation=transformation)

    batch = Batch(data=output['data'], meta=output['meta'])

    filename = split(uri)[1]
    dump_path = f"{dump_dir}_{filename}"
    batch.dump(dump_path)
    print(f'+ Batch from {color(filename, "yellow")} extracted and persisted.')
    print(batch.info())

    return batch.meta


