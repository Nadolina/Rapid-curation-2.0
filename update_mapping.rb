#!/usr/bin/env ruby

require 'optparse'

fasta = ''
table = ''
debug = false
new_mapping = false
chromosome_list = ''

def get_mapping(file)
  mapping = Hash.new
  File.new(file).each_line{|line|
    line.chomp!
    c=line.split
    next unless c[1] =~ /SUPER_\d+/ # do not map sex chromosomes across 
    next if mapping.values.include?(c[1]) # create an artificial 1:1 mapping
    next if mapping.keys.include?(c[0]) # create an artificial 1:1 mapping
    mapping[c[0]]=c[1]
  }
  mapping
end

def create_chromosme_list_line(id)
    /(SUPER_[A-Z0-9]+)(_unloc_\d+)*/.match(id)
    name   = "#{$1}"
    suffix = "#{$2}"
    stripped_name = name.sub("SUPER_",'')
    line = []
    if suffix.length >=1
      line = [name+suffix,stripped_name,'no']
    else
      line = [name,stripped_name,'yes']
    end
    line.join(',')
end

OptionParser.new do |parser|
  parser.banner = "Usage: update_mapping --fasta FASTA_FILE --mashmap_table TABLE_TSV [ --debug | --new_mapping NEW_MAPPING_TSV | --help | --chromosome_list NEW_CHROMOSOME_LIST]"
  parser.on("-f", "--fasta FASTA_FILE") { |f| fasta = f }
  parser.on("-t", "--mashmap_table TABLE_TSV") { |f| table = f }
  parser.on("-d", "--debug") { debug = true }
  parser.on("-n", "--new_mapping NEW_MAPPING_TSV") { |f| new_mapping = f }
  parser.on("-c", "--chromosome_name NEW_CHROMOSOME_LIST") {|f| chromosome_list = f}
  parser.on("-h", "--help") do
    puts parser
    exit
  end
end.parse!

hap2_hap1_mapping = get_mapping(table)

count=1
new_table = File.new(new_mapping,'w') if new_mapping
#new_chrom_file = File.new(chromosome_list,'w') if chromosome_list

File.new(fasta).each_line{|line|
    if />(SUPER_\d+)(_unloc_\d+)*/.match(line)
      name   = "#{$1}"
      suffix = "#{$2}"
      if hap2_hap1_mapping.has_key?(name)
        line = line.sub(name, hap2_hap1_mapping[name])
        $stderr.puts("renaming #{name}#{suffix} => #{hap2_hap1_mapping[name]}#{suffix}") if debug
        new_table.puts([name+suffix, hap2_hap1_mapping[name]+suffix].join("\t")) if new_mapping
        #new_chrom_file.puts(create_chromosme_list_line(hap2_hap1_mapping[name]+suffix)) if chromosome_list
      else
        while hap2_hap1_mapping.reverse_each.to_h.has_key?("SUPER_#{count}")
          count+=1
        end
        id = "SUPER_#{count}"
        line = line.sub(name,id)
        hap2_hap1_mapping[id]=name
        $stderr.puts("renaming #{name}#{suffix} => #{id}#{suffix}") if debug
        new_table.puts( [name+suffix,hap2_hap1_mapping[name]+suffix].join("\t")) if new_mapping
        new_chrom_file.puts(create_chromosme_list_line(hap2_hap1_mapping[name]+suffix)) if chromosome_list
      end
    elsif />(SUPER_\w+)(_unloc_\d+)*/.match(line)
      name   = "#{$1}"
      suffix = "#{$2}"
      #new_chrom_file.puts(create_chromosme_list_line(name+suffix)) if chromosome_list
    end
    print line
}
