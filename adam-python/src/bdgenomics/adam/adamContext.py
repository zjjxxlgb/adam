#
# Licensed to Big Data Genomics (BDG) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The BDG licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from bdgenomics.adam.rdd import AlignmentRecordRDD, \
    CoverageRDD, \
    FeatureRDD, \
    FragmentRDD, \
    GenotypeRDD, \
    NucleotideContigFragmentRDD, \
    VariantRDD
    

class ADAMContext(object):
    """
    The ADAMContext provides functions on top of a SparkContext for loading
    genomic data.
    """


    def __init__(self, sc):
        """
        Initializes an ADAMContext using a SparkContext.

        :param pyspark.context.SparkContext sc: The currently active
        SparkContext.
        """

        self._sc = sc
        self._jvm = sc._jvm
        c = self._jvm.org.bdgenomics.adam.rdd.ADAMContext(sc._jsc.sc())
        self.__jac = self._jvm.org.bdgenomics.adam.api.java.JavaADAMContext(c)


    def loadAlignments(self, filePath):
        """
        Load alignment records into an AlignmentRecordRDD.

        Loads path names ending in:
        * .bam/.cram/.sam as BAM/CRAM/SAM format,
        * .fa/.fasta as FASTA format,
        * .fq/.fastq as FASTQ format, and
        * .ifq as interleaved FASTQ format.
        
        If none of these match, fall back to Parquet + Avro.
        
        For FASTA, FASTQ, and interleaved FASTQ formats, compressed files are supported
        through compression codecs configured in Hadoop, which by default include .gz and .bz2,
        but can include more.

        :param str filePath: The path to load the file from.
        :return: Returns an RDD containing reads.
        :rtype: bdgenomics.adam.rdd.AlignmentRecordRDD
        """

        adamRdd = self.__jac.loadAlignments(filePath)

        return AlignmentRecordRDD(adamRdd, self._sc)


    def loadCoverage(self, filePath):
        """
        Load features into a FeatureRDD and convert to a CoverageRDD.
        Coverage is stored in the score field of Feature.

        Loads path names ending in:
        * .bed as BED6/12 format,
        * .gff3 as GFF3 format,
        * .gtf/.gff as GTF/GFF2 format,
        * .narrow[pP]eak as NarrowPeak format, and
        * .interval_list as IntervalList format.

        If none of these match, fall back to Parquet + Avro.

        For BED6/12, GFF3, GTF/GFF2, NarrowPeak, and IntervalList formats, compressed files
        are supported through compression codecs configured in Hadoop, which by default include
        .gz and .bz2, but can include more.

        :param str filePath: The path to load coverage data from.
        :return: Returns an RDD containing coverage.
        :rtype: bdgenomics.adam.rdd.CoverageRDD
        """

        adamRdd = self.__jac.loadCoverage(filePath)

        return CoverageRDD(adamRdd, self._sc)
        

    def loadContigFragments(self, filePath):
        """
        Load nucleotide contig fragments into a NucleotideContigFragmentRDD.

        If the path name has a .fa/.fasta extension, load as FASTA format.
        Else, fall back to Parquet + Avro.

        For FASTA format, compressed files are supported through compression codecs configured
        in Hadoop, which by default include .gz and .bz2, but can include more.

        :param str filePath: The path to load the file from.
        :return: Returns an RDD containing sequence fragments.
        :rtype: bdgenomics.adam.rdd.NucleotideContigFragmentRDD
        """

        adamRdd = self.__jac.loadContigFragments(filePath)

        return NucleotideContigFragmentRDD(adamRdd, self._sc)


    def loadFragments(self, filePath):
        """
        Load fragments into a FragmentRDD.

        Loads path names ending in:
        * .bam/.cram/.sam as BAM/CRAM/SAM format and
        * .ifq as interleaved FASTQ format.

        If none of these match, fall back to Parquet + Avro.
        For interleaved FASTQ format, compressed files are supported through compression codecs
        configured in Hadoop, which by default include .gz and .bz2, but can include more.

        :param str filePath: The path to load the file from.
        :return: Returns an RDD containing sequenced fragments.
        :rtype: bdgenomics.adam.rdd.FragmentRDD
        """

        adamRdd = self.__jac.loadFragments(filePath)

        return FragmentRDD(adamRdd, self._sc)


    def loadFeatures(self, filePath):
        """
        Load features into a FeatureRDD.

        Loads path names ending in:
        * .bed as BED6/12 format,
        * .gff3 as GFF3 format,
        * .gtf/.gff as GTF/GFF2 format,
        * .narrow[pP]eak as NarrowPeak format, and
        * .interval_list as IntervalList format.

        If none of these match, fall back to Parquet + Avro.

        For BED6/12, GFF3, GTF/GFF2, NarrowPeak, and IntervalList formats, compressed files
        are supported through compression codecs configured in Hadoop, which by default include
        .gz and .bz2, but can include more.

        :param str filePath: The path to load the file from.
        :return: Returns an RDD containing features.
        :rtype: bdgenomics.adam.rdd.FeatureRDD
        """

        adamRdd = self.__jac.loadFeatures(filePath)

        return FeatureRDD(adamRdd, self._sc)


    def loadGenotypes(self, filePath):
        """
        Load genotypes into a GenotypeRDD.

        If the path name has a .vcf/.vcf.gz/.vcf.bgz extension, load as VCF format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :return: Returns an RDD containing genotypes.
        :rtype: bdgenomics.adam.rdd.GenotypeRDD
        """

        adamRdd = self.__jac.loadGenotypes(filePath)

        return GenotypeRDD(adamRdd, self._sc)


    def loadVariants(self, filePath):
        """
        Load variants into a VariantRDD.

        If the path name has a .vcf/.vcf.gz/.vcf.bgz extension, load as VCF format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :return: Returns an RDD containing variants.
        :rtype: bdgenomics.adam.rdd.VariantRDD
        """

        adamRdd = self.__jac.loadVariants(filePath)

        return VariantRDD(adamRdd, self._sc)
