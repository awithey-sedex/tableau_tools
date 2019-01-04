# -*- coding: utf-8 -*-

from ..tableau_base import *
from tableau_datasource import TableauDatasource
from tableau_parameters import TableauParameters
from tableau_document import TableauDocument
import os
import codecs
import xml.etree.ElementTree as etree

class TableauWorkbook(TableauDocument):
    def __init__(self, twb_filename, logger_obj=None):
        TableauDocument.__init__(self)
        self._document_type = u'workbook'
        self.parameters = None
        self.logger = logger_obj
        self.log(u'Initializing a TableauWorkbook object')
        self.twb_filename = twb_filename
        self.xml = None
        # Check the filename
        if self.twb_filename.find('.twb') == -1:
            raise InvalidOptionException(u'Must input a .twb filename that exists')
        self.build_document_objects(self.twb_filename)

    def build_document_objects(self, filename):
        utf8_parser = etree.XMLParser(encoding='utf-8')
        with codecs.open(filename, "rb") as file_handle:
            self.xml = etree.parse(file_handle).getroot()

        self.log(u"Building TableauDatasource objects")
        ds_xml = self.xml.find('./datasources')
        datasource_elements = ds_xml.findall(u'datasource')
        if datasource_elements is None:
            raise InvalidOptionException(u'Error with the datasources from the workbook')
        for datasource in datasource_elements:
            if datasource.get(u'name') == u'Parameters':
                self.log(u'Found embedded Parameters datasource, creating TableauParameters object')
                self.parameters = TableauParameters(datasource, self.logger)
            else:
                ds = TableauDatasource(datasource, self.logger)
                self._datasources.append(ds)

    def add_parameters_to_workbook(self):
        """
        :rtype: TableauParameters
        """
        if self.parameters is not None:
            return self.parameters
        else:
            self.parameters = TableauParameters(logger_obj=self.logger)
            return self.parameters

    def save_file(self, filename_no_extension, save_to_directory=None):
        """
        :param filename_no_extension: Filename to save the XML to. Will append .twb if not found
        :type filename_no_extension: unicode
        :type save_to_directory: unicode
        :rtype: bool
        """
        self.start_log_block()
        try:
            if filename_no_extension.find('.twb') == -1:
                filename_no_extension += '.twb'
            self.log(u'Saving to {}'.format(filename_no_extension))
            with codecs.open(filename_no_extension, 'wb') as file_handle:
                etree.ElementTree(self.xml).write(file_handle, encoding='utf-8', xml_declaration=True)

            self.end_log_block()
            return True

        except IOError as e:
            self.log(u"Error writing to file: {} - {}".format(filename_no_extension, e))
            self.end_log_block()
            raise
