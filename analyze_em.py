# Author: Cameron F. Abrams, <cfa22@drexel.edu>
import pandas as pd
import numpy as np
import yaml
import os
import matplotlib.pyplot as plt
import seaborn as sns
import argparse as ap
from parse_em import get_dataframe, display_nested_dict_keys

def my_box_strip(rootdict,cat,subcats,xlabel="",figsize=(7,5),subcatlabels=[],filename='',ax=None):
    if len(cat)>1:
        # Recurse until we get to the last category in the list
        return my_box_strip(rootdict[cat[0]],cat[1:],subcats,xlabel=xlabel,figsize=figsize,subcatlabels=subcatlabels,filename=filename,ax=ax)
    else:
        df=get_dataframe(rootdict,fetch={cat[0]:subcats})
        if ax==None:
            f,ax=plt.subplots(figsize=figsize)
        yname='category'
        if len(subcatlabels)>0:
            assert len(subcatlabels)==len(subcats)
            mapdict={x:y for x,y in zip(subcats,subcatlabels)}
            def mapfunc(x):
                return mapdict[x]
            df['labels']=df['category'].apply(mapfunc)
            yname='labels'
        sns.boxplot(df,x='counts',y=yname,palette='vlag',fliersize=0,ax=ax)
        sns.stripplot(df,x='counts',y=yname,size=4,color=".3",ax=ax)
        ax.set(ylabel="",xlabel=xlabel)
        ax.xaxis.grid(True)
        if len(filename)>0:
            plt.savefig(filename,bbox_inches='tight')
        return ax

if __name__=='__main__':

    parser=ap.ArgumentParser()
    parser.add_argument('-d',type=str,default='data/data.yml',help='name of input database in YAML format')
    parser.add_argument('--show-depth',type=int,default=0,help='display database to this depth and exit making no graphics')
    parser.add_argument('--seaborn-style',type=str,default='whitegrid')
    parser.add_argument('-od',type=str,default=f'graphics',help='output directory into which I will save images')
    parser.add_argument('-iy',type=str,default=None,help='name of YAML input script describing what plots to generate')
    parser.add_argument('--plotonly',type=str,default=[],nargs='+',help='list of filenames to plot (all if not specified)')

    args=parser.parse_args()
    if not os.path.exists(args.od):
        os.mkdir(args.od)

    with open(args.d,'r') as f:
        db=yaml.safe_load(f)

    plotspecs=[]
    if args.iy:
        with open(args.iy,'r') as f:
            plotspecs=yaml.safe_load(f)

    if args.show_depth>0:
        display_nested_dict_keys(db,maxlevel=args.show_depth)
        exit()

    my_params={
        "axes.spines.right":False,
        "axes.spines.top":False,
        "axes.spines.bottom":False,
        "axes.spines.left":False,
        "ytick.left":False
        }
    sns.set_theme(style=args.seaborn_style,rc=my_params)

    for spec in plotspecs:
        type=spec.get('type','single_box_strip')
        filename=spec.get('filename','')
        assert filename!=''
        if args.plotonly and filename not in args.plotonly:
            print(f'skipping {filename}')
            continue
        if type=='single_box_strip':
            keychain=spec['keychain']
            bars=spec.get('bars',[])
            xlabel=spec.get('xlabel','')
            barlabels=spec.get('barlabels',[])
            filename=spec.get('filename','')
            width=spec.get('width',7)
            special=spec.get('special',[])
            height=len(bars)
            if height==0:
                height=spec.get('height',5)
            fig,ax=plt.subplots(1,1,figsize=(width,height))
            if len(special)==0:
                send_filename=f'{args.od}/{filename}'
            else:
                send_filename=''
            ax=my_box_strip(db,
                    keychain,
                    bars,
                    xlabel=xlabel,
                    subcatlabels=barlabels,
                    filename=send_filename,
                    ax=ax)
            if len(special)>0:
                for cmd in special:
                    eval(cmd)
                plt.savefig(f'{args.od}/{filename}',bbox_inches='tight')
            plt.clf()
            print(f'{type} {filename}')
        elif type=='scatter':
            xdataspec=spec.get('xdataset',{})
            ydataspec=spec.get('ydataset',{})
            xlabel=spec.get('xlabel','')
            ylabel=spec.get('ylabel','')
            filename=spec.get('filename','')
            figsize=spec.get('figsize',(7,5))
            transform=spec.get('transform',{})
            xf=get_dataframe(db,{xdataspec['key']:[xdataspec['values']]})
            yf=get_dataframe(db,{ydataspec['key']:[ydataspec['values']]})
            xscale=xdataspec.get('scaleby',1.0)
            yscale=ydataspec.get('scaleby',1.0)
            xf['counts']*=xscale
            yf['counts']*=yscale
            xdata=xf['counts']
            ydata=yf['counts']
            if transform:
                replace=transform['replace']
                operation=transform['operation']
                if replace=='ydataset':
                    if operation=='y/x':
                        ydata=ydata/xdata
                    elif operation=='1/y':
                        ydata=np.reciprocal(ydata)
            xydf=pd.DataFrame({'x':xdata.to_list(),'y':ydata.to_list()})
            fig,ax=plt.subplots(figsize=figsize)
            sns.scatterplot(xydf,x='x',y='y',ax=ax)
            ax.set_ylabel(ylabel)
            ax.set_xlabel(xlabel)
            plt.savefig(f'{args.od}/{filename}',bbox_inches='tight')
            plt.clf()
            print(f'{type} {filename}')
        else:
            print(f'I do not know how to handle a plot spec of type {type}')

    # one-offs not specified in YAML input
    if not args.plotonly or '03_faculty_salaries.png' in args.plotonly:
        # special stacked salary plots
        bars=['High','Avg','Low']
        fig,ax=plt.subplots(3,1,figsize=(7,len(bars)),height_ratios=[1,1,1.3],sharex=True)
        keychain=['Faculty','Salary','Full']
        ax[0]=my_box_strip(db,keychain,bars,ax=ax[0])
        keychain[-1]='Assoc'
        ax[1]=my_box_strip(db,keychain,bars,ax=ax[1])
        keychain[-1]='Asst'
        bars+=['New hire']
        ax[2]=my_box_strip(db,keychain,bars,ax=ax[2])
        ax[2].set(ylabel="")
        ax[2].set(xlabel='Salaries ($1000/y)')
        ax[2].text(305000,3,'Assistant')
        ax[1].text(305000,2,'Associate')
        ax[2].set_xlim([50000,350000])
        ax[1].set(ylabel="",xlabel="")
        ax[0].set(ylabel="",xlabel="")
        ax[0].text(305000,2,'Full')
        ax[0].set_xlim([50000,350000])
        ax[2].set_xticks(range(50000,400000,50000),[f'{int(x):d}' for x in range(50,400,50)])
        plt.savefig(f'{args.od}/03_faculty_salaries.png',bbox_inches='tight')
        print('03_faculty_salaries.png')
        plt.clf()

    if not args.plotonly or ('14_ug_enrollment_fr_incl.png' in args.plotonly and '15_ug_enrollment_fr_not_incl.png' in args.plotonly):
        # custom box-strips to parse out the
        # different ways of counting enrollment
        undergrad_df=get_dataframe(db,{'Undergrad Program':['Total enrollment']})
        incl_fr_df=get_dataframe(db,{'Undergrad Program':['Total enrollment incl. freshmen?']})
        idf=pd.DataFrame({'category':['Total enrollment']*undergrad_df.shape[0],'counts':undergrad_df['counts']*incl_fr_df['counts']})
        idf.drop(idf[idf["counts"]==0].index,inplace=True)
        ndf=pd.DataFrame({'category':['Total enrollment']*undergrad_df.shape[0],'counts':undergrad_df['counts']*(1-incl_fr_df['counts'])})
        ndf.drop(ndf[ndf["counts"]==0].index,inplace=True)
        ndf
        f,ax=plt.subplots(figsize=(7,1))
        sns.boxplot(idf,x='counts',y='category',palette='vlag',fliersize=0)
        sns.stripplot(idf,x='counts',y='category',size=4,color=".3")
        ax.set(ylabel="")
        ax.xaxis.grid(True)
        ax.set_xlabel('')
        ax.text(-110,0.25,"pgms include freshmen",fontsize=9)
        ax.set_xlim([0,500])
        plt.savefig(f'{args.od}/14_ug_enrollment_fr_incl.png',bbox_inches='tight')
        f,ax=plt.subplots(figsize=(7,1))
        sns.boxplot(ndf,x='counts',y='category',palette='vlag')
        sns.stripplot(ndf,x='counts',y='category',size=4,color=".3")
        ax.set(ylabel="")
        ax.xaxis.grid(True)
        ax.set_xlabel('')
        ax.set_xlim([0,500])
        ax.text(-110,0.25,"pgms do not include freshmen",fontsize=9)
        plt.savefig(f'{args.od}/15_ug_enrollment_fr_not_incl.png',bbox_inches='tight')
        plt.clf()

    if not args.plotonly or '18-01_frac_american_ms_phd.png' in args.plotonly:
        mst=get_dataframe(db,{'Grad Program':['Total # MS']})
        amst=get_dataframe(db,{'Grad Program':['# American MS']})
        srs1=amst['counts']/mst['counts']
        pst=get_dataframe(db,{'Grad Program':['Total # PhD']})
        apst=get_dataframe(db,{'Grad Program':['# American PhD']})
        srs2=apst['counts']/pst['counts']
        cdf=pd.DataFrame({'PhD enrollment':pst['counts'],'frac American PhD':srs2})
        srs=srs1.to_list()+srs2.to_list()
        fracs=pd.DataFrame({'category':['frac American MS']*mst.shape[0]+['frac American PhD']*pst.shape[0],'counts':srs})
        f,ax=plt.subplots(figsize=(7,2))
        sns.boxplot(fracs,x='counts',y='category',palette='vlag',fliersize=0)
        sns.stripplot(fracs,x='counts',y='category',size=4,color=".3")
        ax.set(ylabel="")
        ax.xaxis.grid(True)
        ax.set_xlabel('')
        ax.set_xlim([0,1])
        plt.savefig(f'{args.od}/18-01_frac_american_ms_phd.png',bbox_inches='tight')
        plt.clf()
