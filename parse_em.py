# Author: Cameron F. Abrams, <cfa22@drexel.edu>
"""
Parse 2024 NEMA CHE Chairs Forum Survey responses into a joint
database for analysis and plotting
"""
import pandas as pd
import glob
import numpy as np
import yaml
import os

forbidden_strings=['included above']
def parse_response(filename):
    """ Parses the XLSX file `filename` according to the 2024 NEMA
        CHE Chairs Forum survey 
        
    Parameters:
    -----------
    - filename : str
      name of xlsx file
    
    Returns:
    --------
    A nested dictionary of data extracted from the file
    """
    raw=pd.read_excel(filename)
    results={}
    results['School']=raw.iloc[0,7]
    results['Faculty']={
        'FTE TT':raw.iloc[4,4],
        'FTE NTT':raw.iloc[5,4],
        'FTE Vacant':raw.iloc[6,4],
        'FTE ProfPrac':raw.iloc[27,4],
        'Load/term ProfPrac':raw.iloc[28,4],
        'Typical term course load':raw.iloc[7,4],
        'FTE NTT Teaching':raw.iloc[29,4],
        'Load/term NTT Teaching':raw.iloc[30,4],
        'FTE NTT Research':raw.iloc[31,4],
        'Course buyout reqd to reduce load':raw.iloc[8,4],
        'Salary':{
            'Asst':{
                'High':raw.iloc[12,4],
                'Avg':raw.iloc[13,4],
                'Low':raw.iloc[14,4],
                'New hire':raw.iloc[23,4]
                },
            'Assoc':{
                'High':raw.iloc[15,4],
                'Avg':raw.iloc[16,4],
                'Low':raw.iloc[17,4],
                'New hire':raw.iloc[24,4]
                },
            'Full':{
                'High':raw.iloc[18,4],
                'Avg':raw.iloc[19,4],
                'Low':raw.iloc[20,4],
                'New hire':raw.iloc[25,4]
                }
        },
        'Startup Asst':{ # these may be comma-separated
            'Research area':raw.iloc[34,4],
            'Equipment funding':raw.iloc[35,4],
            'Unrestricted funds':raw.iloc[36,4],
            'Summer salary':raw.iloc[37,4],
            'Grad student support':raw.iloc[38,4],
            'Teaching load':raw.iloc[39,4],
            'Relocation funds':raw.iloc[40,4],
            'Travel funds':raw.iloc[41,4],
            'Other support':raw.iloc[42,4],
            'Total package':raw.iloc[43,4]
        }
    }
    results['Research']={
        'Annual expenditures':raw.iloc[46,4],
        'Number of ISI pubs':raw.iloc[47,4],
        'Overhead rate(%)':raw.iloc[48,4],
        'frac OHR dept':raw.iloc[49,4],
        'frac OHR PI':raw.iloc[50,4]
    }
    results['Budget']={
        'Faculty':raw.iloc[54,4],
        'NTT Istr/ProfPrac':raw.iloc[55,4],
        'Staff':raw.iloc[56,4],
        'TA Support':raw.iloc[57,4],
        'Operating/Current exp':raw.iloc[58,4],
        'Hard budget funds':raw.iloc[60,4],
        'Student fees':raw.iloc[61,4],
        'Add\'l soft money':raw.iloc[62,4],
        'Total Hard+Soft':raw.iloc[63,4],
    }
    results['Staff']={
        'FTE total admin':raw.iloc[66,4],
        'FTE grad student svcs':raw.iloc[67,4],
        'FTE ugrad student svcs':raw.iloc[68,4],
        'FTE grants staff':raw.iloc[69,4],
        'FTE technical staff':raw.iloc[70,4],
        'FTE facilities staff':raw.iloc[71,4],
        '# development staff':raw.iloc[72,4],
        '# staff FTE supported at college/campus level':raw.iloc[73,4],
        'Avg postdoc salary':raw.iloc[74,4],
        '12-mo cost of PhD student':raw.iloc[75,4]
    }
    results['Undergrad Program']={
        'Common Freshman Year?':raw.iloc[78,4],
        'Total enrollment':raw.iloc[79,4],
        'Total enrollment incl. freshmen?':raw.iloc[80,4],
        '% URM':raw.iloc[81,4],
        '% Female':raw.iloc[82,4],
        '% Intl':raw.iloc[83,4],
        'Total UG graduated':raw.iloc[85,4],
        'UG to industry':raw.iloc[86,4],
        'UG to grad school':raw.iloc[87,4],
        'UG ro prof school':raw.iloc[88,4],
        'UG unemployed':raw.iloc[89,4],
        'UG returned to home country':raw.iloc[90,4],
        'UG to other':raw.iloc[91,4],
        '# grads w at least one coop/internship':raw.iloc[92,4],
        '# grads w research experience':raw.iloc[93,4],
        '# grads w who studied abroad':raw.iloc[94,4],
        '# grads w no outside classroom experience':raw.iloc[95,4],
    }
    results['Grad Program']={
        'Total MS/PhD enrollment':raw.iloc[98,4],
        'Total # MS':raw.iloc[99,4],
        '# American MS':raw.iloc[100,4],
        'Total # PhD':raw.iloc[101,4],
        '# American PhD':raw.iloc[102,4],
        'Total # US minority grad students':raw.iloc[103,4],
        '# Female grad students':raw.iloc[104,4],
        'Total # support GTA/GRA':raw.iloc[105,4],
        '# Dept supported TAs':raw.iloc[106,4],
        '# Non-dept supported TAs':raw.iloc[107,4],
        '# Research Assts supported':raw.iloc[108,4],
        '# Students w outside fellowships':raw.iloc[109,4],
        '# For-pay masters students':raw.iloc[110,4],
        '# Unsupported/other':raw.iloc[111,4],
        'Months of non-research support for new PhD students':raw.iloc[112,4],
        'Stipends':{
            'MS':raw.iloc[114,4],
            'PhD':raw.iloc[115,4]
        },
        'Avg annual cost to student':raw.iloc[116,4],
        '$ signing bonus':raw.iloc[117,4],
        'Total MS degrees granted':raw.iloc[118,4],
        '# MS to industry':raw.iloc[119,4],
        '# MS to academia':raw.iloc[120,4],
        '# MS to PhD':raw.iloc[121,4],
        '# MS to other prof school':raw.iloc[122,4],
        '# MS to govt':raw.iloc[123,4],
        '# MS to other (incl return home cntry)':raw.iloc[124,4],
        '# MS unemployed':raw.iloc[125,4],
        '# MS unknown':raw.iloc[126,4],
        'BS to MS average time to degree, months':raw.iloc[128,4],
        'Total PhD degrees granted':raw.iloc[130,4],
        '# PhD to industry':raw.iloc[131,4],
        '# PhD to academia/postdoc':raw.iloc[132,4],
        '# PhD to prof school':raw.iloc[133,4],
        '# PhD to govt':raw.iloc[134,4],
        '# PhD to other':raw.iloc[135,4],
        '# PhD unemployed':raw.iloc[136,4],
        '# PhD unknown':raw.iloc[137,4],
        'BS to PhD time to degree, months':raw.iloc[139,4],
        'MS to PhD time to degree, months':raw.iloc[140,4],
        'PhD Coursework':{
            'total ChE formal lecture hours':raw.iloc[143,4],
            'total formal lecture hours':raw.iloc[144,4],
            'total required credit hours':raw.iloc[145,4],
            'average time to complete coursework':raw.iloc[146,4],
            'Deficiency ChE coursework hrs':raw.iloc[147,4]
        }
    }
    return results

def str2data(a_string):
    """ Custom conversion of strings to data """
    if ',' in a_string:
        # Some users put comma-separated values in a cell; this
        # parses them into a list and recursively operates on
        # each resulting element
        result=[str2data(x.strip()) for x in a_string.split(',')]
        return result
    elif a_string.lower() in ['true','yes','y','for sure','ok']:
        return True
    elif a_string.lower() in ['false','no','n','no way, man','aw hell no']:
        return False
    elif '-' in a_string:
        # some respondents indicate a range between two limits
        # so I just return the average if there are two. If
        # for some reason there a sequence of numbers separated
        # by dashes, I just return the max; if no numeric data
        # at all is detected, just return the original string
        tokens=a_string.split('-')
        if all([t.isnumeric() for t in tokens]):
            if len(tokens)==2:
                return float(sum(map(int,tokens))/2)
            else:
                return float(max(map(int,tokens)))
        return a_string
    elif a_string.replace('.','',1).isdigit():
        # string is numerical and can be a float or integer
        if '.' in a_string:
            return float(a_string)
        else:
            return int(a_string)
    elif '.' in a_string and a_string.endswith('M'):
        # Some go-getters use the capital M to mean
        # "multiplied by one million" so let's fix that
        # little nasty shall we
        a_string=a_string[:-1]
        assert a_string.replace('.','',1).isdigit()
        return 1.e6*float(a_string)
    # print(f'I am assuming {a_string} is a raw string')
    return a_string

def completeness(a_dict):
    """ Compute the fractional completeness of the response; 
    Yes it is recursive because we use a nested dictionary! """
    data_count=0
    response_count=0
    ignored={}
    for k,v in a_dict.items():
        if type(v)==dict:
            bdc,brc,bignored=completeness(v)
            data_count+=bdc
            response_count+=brc
            if len(bignored)>0:
                ignored[k]=bignored
        else:
            data_count+=1
            if type(v)==float:
                if not np.isnan(v):
                    response_count+=1
                else:
                    ignored[k]=v
            elif type(v)==str:
                if len(v)>0:
                    response_count+=1
                else:
                    ignored[k]=v
            else:
                response_count+=1
    return data_count,response_count,ignored

def healset(a_list):
    """ Data healing; this is where raw strings in the response cells
    are converted to data and full datasets are generated """
    healed=[]
    last_type=None
    # is_mixed=False
    for x in a_list:
        if type(x)==dict:
            healed.append(x)
            if not last_type:
                last_type=dict
        else:
            if type(x)==str:
                if not last_type:
                    last_type=str
                if len(x)>0 and not x.isspace():
                    # assume this is a yes/no answer
                    p=str2data(x)
                    if type(p)==bool:
                        healed.append(1 if p else 0)
                    elif type(p)==list:
                        if all([type(x)==int or type(x)==float for x in p]):
                            healed.append(sum(p)/len(p))
                        else:
                            healed.append(p)
                    else:
                        if not p in forbidden_strings:
                            healed.append(p)
                        else:
                            healed.append(np.nan)
                else:
                    healed.append(np.nan)
            elif type(x)==int or type(x)==float:
                if not last_type:
                    last_type=type(x)
                healed.append(x)
            else:
                print(f'What do I do with [{x}] of type {type(x)}')
    return healed

def joint(some_dicts):
    """ Joins all dicts of data *points* 
    from all xlsx files into a single joint dict 
    of data *sets* """
    jointdict={}
    nresponses=len(some_dicts)
    for k,v in some_dicts[0].items():
        dataset=healset([d[k] for d in some_dicts])
        assert len(dataset)==nresponses
        if len(dataset)==0:
            jointdict[k]=dict(msg='No data',dataset=[])
        elif type(dataset[0])==dict:
            jointdict[k]=joint(dataset)
        elif type(dataset[0])==str:
            jointdict[k]=dict(dataset=dataset)
        else:
            jointdict[k]=dict(dataset=list(dataset))
    return jointdict

def display_nested_dict_keys(adict,level=0,maxlevel=None):
    """ Recursively displays keys in a nested dictionary 
    
    Parameters:
    -----------
    level : int
      current depth of keys being displayed
    maxlevel : int
      maximum depth to display; if set to None, display all
      
    """
    for n,v in adict.items():
        print(f'{level*" "}{n}')
        if type(v)==dict and (maxlevel==None or level<=maxlevel):
            display_nested_dict_keys(v,level=level+1,maxlevel=maxlevel)

def getall(data_directory='.',schools_yml='schools.yml',data_yml='data.yml'):
    responses=glob.glob(os.path.join(data_directory,'*.xlsx'))
    data={}
    avgcomplete=0.0
    for r in responses:
        results=parse_response(r)
        data[results['School']]=results
        nd,nr,ignored=completeness(results)
        print(f'{results["School"]}: {nr/nd*100:.2f}% complete')
        avgcomplete+=nr/nd
    print(f'Average completeness: {avgcomplete/len(responses)*100:.2f} among {len(data)} responses')
    j=joint([response for response in data.values()])

    with open(schools_yml,'w') as outfile:
        yaml.dump(j['School'],outfile)
    del j['School']
    with open(data_yml, 'w') as outfile:
        yaml.dump(j,outfile,sort_keys=False)
    return j

def get_dataframe(adict,fetch={}):
    """ Return the dataset associated with the key:value pair in 
        dict parameter fetch """
    category=list(fetch.keys())[0]
    categories=list(fetch.values())[0]
    if len(categories)==0:
        categories=list(adict[category].keys())
        print(f'defaulting to all categories: {categories}')
    tmp_cat=categories[:]
    for x in tmp_cat:
        if 'dataset' not in adict[category][x] or len(adict[category][x]['dataset'])==0:
            categories.remove(x)
    data=[np.array(adict[category][x]['dataset'],dtype=float) for x in categories]
    maxlen=max([len(x) for x in data])
    catcol=[]
    for i in range(len(data)):
        catcol+=maxlen*[categories[i]]
    data=np.array(data)
    data=data.flatten()
    return pd.DataFrame({'category':catcol,'counts':data})

if __name__=='__main__':
    import argparse as ap

    parser=ap.ArgumentParser()
    parser.add_argument('-d',help='directory containing survey responses',default='.',type=str)
    parser.add_argument('-sf',help='name of school name list output',default='data/schools.yml',type=str)
    parser.add_argument('-df',help='name of data output',default='data/data.yml',type=str)
    args=parser.parse_args()

    getall(data_directory=args.d,schools_yml=args.sf,data_yml=args.df)
