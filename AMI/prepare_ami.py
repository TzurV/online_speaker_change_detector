'''
based on https://github.com/gcunhase/AMICorpusXML
'''

import os
import argparse
from pathlib import Path
from collections import defaultdict
from xml.dom import minidom

# get all xml files and group them
def get_words_xml_files_list(ami_xml_words_dir):
    transcript_speaker_files = [f for f in os.listdir(ami_xml_words_dir) if f.endswith('.xml')]
    print(f"{len(transcript_speaker_files)} transcription file found")

    # Group speaker files by meeting
    group_speaker_files = defaultdict(list)
    for t in transcript_speaker_files:
        meeting = t.split('.')[0]
        if bool(group_speaker_files[meeting]):
            group_speaker_files[meeting].append(t)
        else:
            group_speaker_files[meeting] = [t]
    print(f"{len(group_speaker_files)} number of groups")

    return transcript_speaker_files, group_speaker_files


def create_new_segment(speaker, elem):
    starttime = elem.getAttributeNode('starttime').value
    endtime = elem.getAttributeNode('endtime').value
    seg_dic = {'speaker':speaker, 'starttime':float(starttime), 'endtime':float(endtime)}
    return seg_dic

def creat_speech_segments(XML_data, speaker):
    segments = list()
    for indx, elem in enumerate( XML_data.getElementsByTagName('w')):
        if elem.hasAttribute('punc') or\
            'starttime' not in elem.attributes.keys():
            continue
        if not segments or\
            segments[-1]['endtime'] != float(elem.getAttributeNode('starttime').value):
            # create new segment
            segments.append(create_new_segment(speaker, elem))

        else:
            # update last segment
            segments[-1]= {'speaker':speaker, 
                           'starttime':segments[-1]['starttime'], 
                           'endtime':float(elem.getAttributeNode('endtime').value)}

    return segments

def process_group(ami_xml_words_dir, group, xml_files):
    print(f"Group {group}:{xml_files}")

    speakers_speech_segments = list()
    for file in xml_files:
        speaker = file.split('.')[1]
        XML_data = minidom.parse(os.path.join(ami_xml_words_dir, file))
        speakers_speech_segments += creat_speech_segments(XML_data, speaker)
        
    print(f"\t>Total number of segments {len(speakers_speech_segments)}")
    
    #xml_info = [minidom.parse(os.path.join(ami_xml_words_dir, file)) for file in xml_files]
    #print(xml_info)
    # items =xml_info[0].getElementsByTagName('w')
    # ------------- XML line ----
    # <w nite:id="EN2001a.A.words0" starttime="5.57" endtime="5.94">Okay</w>
    # word -> print(items[0].firstChild.data)
    #>> <DOM Text node "'Okay'">
    #>> None
    # print(items[0].attributes.keys())
    #>> dict_keys(['nite:id', 'starttime', 'endtime'])
    #>> None
    # print(items[0].getAttributeNode('starttime').value)
    #>> 5.57
    #>> None


def process(args):
    if not os.path.exists(args.ami_xml_words_dir):
        raise Exception(f"path not found {args.ami_xml_words_dir}")

    all_xml_files_list, group_speaker_files = get_words_xml_files_list(args.ami_xml_words_dir)
        
    for group in group_speaker_files:
        process_group(args.ami_xml_words_dir, group, group_speaker_files[group])
        
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare AMI Corpus for speaker switch detection.')

    parser.add_argument('--ami_xml_words_dir', type=str, required=True,
                        help='AMI Corpus download words directory')    
    parser.add_argument('--output_dir', type=str, default='out/',
                        help='output directory')
    
    command_line = "--ami_xml_words_dir E:\\Tzur\\optimeet\\Corpora\\AMI\\ami_public_manual_1.6.2\\words"    
    args = parser.parse_args(command_line.split())
    process(args)
    
    pass
