library(readr)
library(lsa)
library(ISLR)
library(stringr)
library(stringi)
library(dplyr)
library(tibble)
library(tidyverse)
library(wordcloud)
library(matrixStats)
library(dendextend)

WORK.DIR = "/Users/dcody/Desktop/Data_Science2/Project/Code/Descriptions_Project/Item1_Analysis"
setwd(WORK.DIR)

data_dir = 'Description_Data/'
visuals_dir = 'Visuals/'
num_clustres = 10 #number of clusters to assign the data too
tfidf_read = read_csv(paste(data_dir,'tfidf_2019.csv',sep = ""))
tfidf_df = tfidf_read[,-(1:2)]
cos_dist = as.dist(1-cosine(as.matrix(tfidf_df))) #description distance object

#test linkage methods
hc_complete=hclust(cos_dist, method="complete")
hc_average = hclust(cos_dist, method="average")
hc_single = hclust(cos_dist, method="single")
hc_centroid = hclust(cos_dist, method="centroid")

par(mfrow = c(2,2))
plot(hc_complete, main='Complete Linkage', xlab="", sub ="", cex=.4)
plot(hc_average, main='Average Linkage', xlab="", sub ="", cex=.4)
plot(hc_single, main='Single Linkage', xlab="", sub ="", cex=.4)
plot(hc_centroid, main='Centroid Linkage', xlab="", sub ="", cex=.4)

#heriarichincal clustering with complete linkage
hc=hclust(cos_dist, method='complete')
hc_clusters = cutree(hc, k = num_clustres)
#k-means CLustering 
km.out = kmeans(cos_dist,num_clustres,nstart = 10)
km.out$tot.withinss #tested nstart up to nstart =100. Min tot.withinss found at nstart = 10
km_clusters = km.out$cluster

#compare kmeans and heriarchical clustering 
table(hc_clusters,km_clusters)
plot(table(hc_clusters,km_clusters), main = "Kmeans & Heirarchical Similarity")


#heriarcihcal clustering visuals 
plot(hc, main='2019 Dendrogram', xlab="", sub ="", hang = FALSE,cex=.9)
heatmap(as.matrix(cos_dist),
        main = '2019',
        cexRow = .3, cexCol = .3, 
        labRow=names(tfidf_df),
        labCol=names(tfidf_df))


#Sector breakdown of cluster
sector_map = read_csv("Description_Data/Sector_Map_Clean.csv")
cluster_df = data.frame(hc_clusters)
cluster_df['Ticker'] = rownames(cluster_df)
company_sector_cluster_df = merge(cluster_df,sector_map, by=c('Ticker'))
#save file 
write_csv(company_sector_cluster_df, file = 'R_Output_Data/company_sector_cluster.csv')

#PCA Analysis 
pr.out = prcomp(t(tfidf_df))
term_pca_weights = data.frame(pr.out$rotation)
rownames(term_pca_weights) = unlist(tfidf_read[,1]) #row names = terms
pca_scores = pr.out$x

#pca plots
#colored by cluster
par(mfrow = c(1,2))
plot(pca_scores[,1:2], col = hc_clusters,
     main = "PCA 1 & PCA 2 \n Colored by Cluster", 
     xlab="Z1", ylab="Z2")
plot(pca_scores[,c(1,3)], col = hc_clusters,
     main = "PCA 1 & PCA 3 \n Colored by Cluster", 
     xlab="Z1", ylab="Z3")

#scree plots
pr.var = pr.out$sdev^2
#PVE
pve = pr.var/sum(pr.var) #PVE OF EACH PC
cumsum(pve) #cumulative PVE

par(mfrow = c(2,2))
plot(pve, xlab="Principal Component", ylab="Proportion of Variance Explained", ylim=c(0,1), type='b') 
plot(cumsum(pve), xlab="Principal Component", ylab ="Cumulative PVE", ylim=c(0,1), type='b')
plot(pve[c(1:20)], xlab="Principal Component", ylab="Proportion of Variance Explained", ylim=c(0,1), type='b') 
plot(cumsum(pve[c(1:20)]), xlab="Principal Component", ylab ="Cumulative PVE", ylim=c(0,1), type='b')


#plot top phis for dim 1, 2, 3, 4
top_10_PC1 = top_n(term_pca_weights['PC1'],n =10)
top_10_PC2 = top_n(term_pca_weights['PC2'],n =10)
top_10_PC3 = top_n(term_pca_weights['PC3'],n =10)
top_10_PC4 = top_n(term_pca_weights['PC4'],n =10)
bottom_10_PC1 = top_n(term_pca_weights['PC1'],n =-10)
bottom_10_PC2 = top_n(term_pca_weights['PC2'],n =-10)
bottom_10_PC3 = top_n(term_pca_weights['PC3'],n =-10)
bottom_10_PC4 = top_n(term_pca_weights['PC4'],n =-10)


par(mfrow = c(2,2))
barplot(top_10_PC1[,1],main = 'Top 10 PC1', 
        names.arg = rownames(top_10_PC1), 
        horiz = TRUE,las= 2,cex.names= .6)
barplot(bottom_10_PC1[,1],main = 'Bottom 10 PC1', 
        names.arg = rownames(bottom_10_PC1), 
        horiz = TRUE,las= 2,cex.names= .6)
barplot(top_10_PC2[,1],main = 'Top 10 PC2', 
        names.arg = rownames(top_10_PC2), 
        horiz = TRUE,las= 2,cex.names= .6)
barplot(bottom_10_PC2[,1],main = 'Bottom 10 PC2', 
        names.arg = rownames(bottom_10_PC2), 
        horiz = TRUE,las= 2,cex.names= .6)


par(mfrow = c(2,2))
barplot(top_10_PC3[,1],main = 'Top 10 PC3', 
        names.arg = rownames(top_10_PC3), 
        horiz = TRUE,las= 2,cex.names= .6)
barplot(bottom_10_PC3[,1],main = 'Bottom 10 PC3', 
        names.arg = rownames(bottom_10_PC3), 
        horiz = TRUE,las= 2,cex.names= .6)
barplot(top_10_PC4[,1],main = 'Top 10 PC4', 
        names.arg = rownames(top_10_PC4), 
        horiz = TRUE, las= 2,cex.names= .6)
barplot(bottom_10_PC4[,1],main = 'Bottom 10 PC4', 
        names.arg = rownames(bottom_10_PC4), 
        horiz = TRUE, las= 2,cex.names= .6)


#word clouds 
cluster_df =  t(data.frame(hc_clusters))
max_num_cluster = max(cluster_df)
for (cluster_num in seq(1:max_num_cluster)){
  cluster_members = c()
  for (ticker in colnames(cluster_df)){
    if (cluster_df[,ticker] == cluster_num)
      {cluster_members = append(cluster_members,ticker)}#end if cluster assignment = cluster_num
  }#end ticker loop
  
  file_name = paste(as.character(cluster_num),'_Custer_WordCloud.jpeg',sep = "")
  word_cloud_dir = paste(visuals_dir,'WordClouds/',sep ="")
  jpeg(paste(word_cloud_dir,file_name,sep=""))
  
  cluster_sub_data = tfidf_df[cluster_members]
  AVG_TFIDF = c(rowMeans(as.matrix(cluster_sub_data)))
  terms = tfidf_read[,1]
  word_cloud_data = data.frame(terms, AVG_TFIDF)
  wordcloud(words = word_cloud_data[,1],freq = word_cloud_data[,2], max.words = 100,
            random.order=FALSE, rot.per=0.35,
            colors=brewer.pal(8, "Dark2"))
  
  dev.off()
} #end cluster num loop


#Tanglegram


returns_read = read_csv("Description_Data/2019_Returns.csv")[-(1),-(1:2)] #remove first na row and idf and dates columns
returns_clean = returns_read[ , colSums(is.na(returns_read)) < nrow(returns_read)] #remove na columns 
cor_matrix = 1 - cor(returns_clean)
cor_dist =as.dist(cor_matrix)
hc_cor=hclust(cor_dist, method="complete")
cor_clusters = cutree(hc_cor, k = num_clustres)
#plot(hc_cor, main='Return Correlation Clusters', xlab="", sub ="", cex=.4)

#Recluster tfidfs so the same tickers are in the returns clusters
tickers_to_use = names(returns_clean)
tfidf_df_small = tfidf_df[tickers_to_use]
cos_dist = as.dist(1-cosine(as.matrix(tfidf_df_small)))
tfidf_hc=hclust(cos_dist, method='complete')
tfidf_clusters = cutree(hc, k = num_clustres)
tfidf_dend = as.dendrogram(tfidf_hc)#dendrogram for cluster compare



return_cor_dend = as.dendrogram(hc_cor)
dends = dendlist(tfidf_dend,return_cor_dend)
entanglement(dends)
tanglegram(dends,sort=TRUE, main_left = 'Description Similarity', main_right = 'Return Correlation',
           cex_main = 1.5,
           lab.cex= .6,k_labels = 8,k_branches = 8, hang = FALSE ,rank_branches = TRUE)

#compare correlation clusters and tfidf clusters
#Match tickers in dataframe 
cor_cluster_df = as.data.frame(cor_clusters)
cor_cluster_df['Ticker'] = rownames(cor_cluster_df)
tfidf_cluster_df = as.data.frame(hc_clusters) 
tfidf_cluster_df['Ticker'] = rownames(tfidf_cluster_df)
Cor_and_TFIDF_Clusters = merge(tfidf_cluster_df,cor_cluster_df, by = 'Ticker')
plot(table(Cor_and_TFIDF_Clusters$hc_clusters,Cor_and_TFIDF_Clusters$cor_clusters), main = "Return Correlation & Description Terms Clusters Similarity")
