# https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount.py
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""A word-counting workflow."""

# pytype: skip-file

# beam-playground:
#   name: WordCount
#   description: An example that counts words in Shakespeare's works.
#   multifile: false
#   pipeline_options: --output output.txt
#   context_line: 87
#   categories:
#     - Combiners
#     - Options
#     - Quickstart
#   complexity: MEDIUM
#   tags:
#     - options
#     - count
#     - combine
#     - strings

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.runners.runner import PipelineResult

from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from datetime import date, datetime
import json
from google.cloud import storage


class WordExtractingDoFn(beam.DoFn):
  """Parse each line of input text into words."""
  def process(self, element):
    storage_client = storage.Client()

    """Returns an iterator over the words of this element.

    The element is a line of text.  If the line is blank, note that, too.

    Args:
      element: the element being processed

    Returns:
      The processed element.
    """

    class SchemaRecord(BaseModel):
      EMPRESA: Optional[str] = None
      FECHA_JORNADA: Optional[date] = None
      TIPO_FLOTA: Optional[str] = None
      ID_PARADA: str
      TIPO_PARADA: Optional[str] = None
      ESTADO_PARADA: Optional[str] = None
      ID_VIAJE: str
      ESTADO_VIAJE: Optional[str] = None
      INICIO_HORARIO_1: Optional[str] = None
      FIN_HORARIO_1: Optional[str] = None
      INICIO_VISTA_PLANIFICADO: Optional[datetime] = None
      FIN_VISTA_PLANIFICADO: Optional[datetime] = None
      FECHA_TRACE_PLANIFICADO: Optional[datetime] = None
      REALIZADO_TRACE: Optional[datetime] = None
      ID_COD_REPORTE: Optional[int] = None
      SERVER: Optional[str] = None
      NOW: Optional[datetime] = None
      DEPOSITO_SALIDA: Optional[str] = None
      CLIENTE_ORDEN: Optional[str] = None
      TIPO_OPERACION: Optional[str] = None
      PLACA: Optional[str] = None
      INICIO_REAL_VIAJE: Optional[datetime] = None
      DEPOSITO_LLEGADA: Optional[str] = None
      RAZON_SOCIAL_TRANSPORTE: Optional[str] = None
      ETA_INICIO_PLAN: Optional[datetime] = None
      ETA_FIN_PLAN: Optional[datetime] = None
      PROVINCIA: Optional[str] = None
      PARTIDO: Optional[str] = None
      LOCALIDAD: Optional[str] = None
      COD_TIENDA: Optional[str] = None
      CLIENTE: Optional[str] = None
      REFERENCIA_ADICIONAL_PARADA: Optional[str] = None
      LAST_PARADA_TRACE_ESTADO: Optional[str] = None

      # Validador que convierte cadenas vacías en None usando Pydantic V2
      @field_validator('*', mode='before')
      def empty_strings_to_none(cls, v):
          if isinstance(v, str) and v.strip() == "":
              return None
          return v
      
    record = json.loads('{"ID_PARADA": "JBRL", "ID_VIAJE": "123" }')
    valid_record = SchemaRecord(**record)
    
    return re.findall(r'[\w\']+', element, re.UNICODE)


def run(argv=None, save_main_session=True) -> PipelineResult:
  """Main entry point; defines and runs the wordcount pipeline."""
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--input',
      dest='input',
      default='gs://dataflow-samples/shakespeare/kinglear.txt',
      help='Input file to process.')
  parser.add_argument(
      '--output',
      dest='output',
      required=True,
      help='Output file to write results to.')
  known_args, pipeline_args = parser.parse_known_args(argv)

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

  pipeline = beam.Pipeline(options=pipeline_options)

  # Read the text file[pattern] into a PCollection.
  lines = pipeline | 'Read' >> ReadFromText(known_args.input)

  counts = (
      lines
      | 'Split' >> (beam.ParDo(WordExtractingDoFn()).with_output_types(str))
      | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
      | 'GroupAndSum' >> beam.CombinePerKey(sum))

  # Format the counts into a PCollection of strings.
  def format_result(word, count):
    return '%s: %d' % (word, count)

  output = counts | 'Format' >> beam.MapTuple(format_result)

  # Write the output using a "Write" transform that has side effects.
  # pylint: disable=expression-not-assigned
  output | 'Write' >> WriteToText(known_args.output)

  # Execute the pipeline and return the result.
  result = pipeline.run()
  result.wait_until_finish()
  return result


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()