//
//  bdfs.cpp
//  
//
//  Created by Sai teja Varanasi on 21/10/21.
//

#include <iostream>
#include <stdlib.h>
#include <time.h>
using namespace std;
class array_s{
public:
    int *a;
    int type;
    int last;
    array_s(int p,int atype){
        a=new int[p];
        type=atype;
        last=0;
    }
    void add(int x){
        a[last]=x;
        last++;
    }
    int give(){
        if(type==0){
            last--;
            return a[last];
        }
        if(type==1){
            int ans=a[0];
            for(int i=1;i<last;i++){
                a[i-1]=a[i];
            }
            last--;
            return ans;
        }
        cout<<"wtf"<<endl;
    }
    bool is_empty(){
        return last==0;
    }
};
class Graph{
public:
    int **a;
    int v;
    int e;
    Graph(int x){
        a=new int*[x];
        for(int i=0;i<x;i++){
            a[i]=new int[x];
        }
        v=x;
        for(int i=0;i<v;i++){
            for(int j=0;j<v;j++){
                a[i][j]=0;
            }
        }
        gen_rand();
    }
    void gen_rand(){
        e=2*v;
        for(int i=0;i<e;i++){
            int num=rand()%(v*v);
            int x_coord=num/v;
            int y_coord=num%v;
            while(a[x_coord][y_coord]==1||x_coord==y_coord){
                 num=rand()%(v*v);
                 x_coord=num/v;
                 y_coord=num%v;
            }
            a[x_coord][y_coord]=1;
            a[y_coord][x_coord]=1;
        }
        for(int i=0;i<v;i++){
            for(int j=0;j<v;j++){
                cout<<a[i][j]<<" ";
            }
            cout<<endl;
        }
        
    }
    void graph_search(int type,int start,int* record){
        array_s obj(v,type);
        int* visited=new int[v];
        for(int i=0;i<v;i++){
            visited[i]=0;
        }
        search(obj,visited,start,record);
    }
    void search(array_s obj,int *visited,int start,int* record){
        int level[v];
        level[start]=0;
        obj.add(start);
        int vop=0;
        while(!obj.is_empty()){
            int x=obj.give();
            record[vop]=x;
            cout<<record[vop]<<"-->";
            vop++;
            visited[x]=1;
            for(int i=0;i<v;i++){
                if(a[x][i]==1&&visited[i]==0){
                    level[i]=level[x]+1;
                    visited[i]=1;
                    obj.add(i);
                }
                else if(a[x][i]==1&&visited[i]==1){
                    if(level[i]==level[x]){
                        cout<<endl;
                        cout<<"internally connected brach"<<endl;
                        cout<<"("<<x<<"-"<<i<<")"<<endl;
                        return;
                    }
                }
            }
        }
        cout<<"one component ended"<<endl;
        for(int i=0;i<v;i++){
            if(visited[i]==0&&i!=start){
                search(obj,visited,i,record);
                break;
            }
        }
    }
    
};
int main(){
    Graph g(6);
    srand(time(0));
    int record[6];
    g.graph_search(0,1,record);
}
