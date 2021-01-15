from reportlab.lib import colors
from Bio import SeqIO
from Bio.Graphics.GenomeDiagram import *

gb_fh = open(r'''C:\Users\sayya\PycharmProjects\Coding-Challenge-S21\Genome.gb''', "r")

# Parse and print name and features to help
# estimate features present in genome diagram

for gb_record in SeqIO.parse(gb_fh, "genbank"):
    print("Name: %s, Features: %i" % (gb_record.name, len(gb_record.features)))
    print(repr(gb_record.seq))

# Create two sets of Feature objects to hold
# "gene" and "CDS" type Features objects

fs_genes = FeatureSet(name="TCSV Feature Set- Genes")
fs_CDS = FeatureSet(name="TCSV Feature Set- CDS")

# Initialize two lists to hold separated Feature objects

fs_genes_list = []
fs_CDS_list = []

# Separate and append Feature objects to initialized lists
# in order to ease creation of features

for record in gb_record.features:
    if record.type == "gene":
        fs_genes_list.append(record)
    elif record.type == "CDS":
        fs_CDS_list.append(record)

# **Use with lists we initialized earlier** Dictionary (index : [arrowhead_height, color])
# containing data regarding graphical output for each "gene" type feature object

visuals_dict = {
    0: [0.6, colors.darkred],
    1: [0.3, colors.red],
    2: [0.9, colors.limegreen],
    3: [0.6, colors.lightgreen],
    4: [0.3, colors.darkgreen]
}

# Loop over one of the lists (One coding seqeuence (CDS)/ gene), assign graphical data
# and add new feature to FeatureSets

for index in range(len(fs_genes_list)):
    fs_genes.add_feature(feature=fs_genes_list[index], label=True, label_size=16, label_angle=-90,
                         color=visuals_dict[index][1], label_position="middle", sigil="ARROW",
                         label_strand=-1, arrowshaft_height=visuals_dict[index][0], border=colors.black)
    fs_CDS.add_feature(feature=fs_CDS_list[index], label=False, color=colors.lightblue, border=colors.black,
                       strand=-1)

# Create a Track for the gene type FeatureSet and another for the CDS type FeatureSet
# Add FeatureSets to Tracks

genes_track = Track(name="TCSV Genes Track", scale=True, scale_color=colors.lightgrey, scale_ticks=True)
genes_track.add_set(fs_genes)
CDS_track = Track(name="TCSV CDS Track", scale=False)
CDS_track.add_set(fs_CDS)

# Create a Diagram object and add Tracks to this object

gdd = Diagram(name="TCSV Diagram")
gdd.add_track(genes_track, 1)
gdd.add_track(CDS_track, 2)

# Draw and write Diagram to file

gdd.draw(
   format="circular", orientation="landscape", pagesize='A4', tracklines=True, circular=True, circle_core=0.5)
gdd.write(filename=r'''C:\Users\sayya\PycharmProjects\Coding-Challenge-S21\TCSV_Diagram_PDF.pdf''', output="PDF")
gdd.write(filename=r'''C:\Users\sayya\PycharmProjects\Coding-Challenge-S21\TCSV_Diagram_PNG.png''', output="PNG")