rm(list=ls())


library(ggplot2)
library(NbClust)
library(factoextra)
library(fpc)
library(dbscan)
library(dplyr)
library(cluster)

# change the path to where you saved the file
Clean_Korea <- read.csv("~/Documents/Classes/depaul/Korea/Data/WorldBank_GDP/Korea_GDPMacro_Data/Clean_Korea.csv")

rownames(Clean_Korea) = Clean_Korea$Year

# Remove X, Year, GDP
data = Clean_Korea[c(-1,-2, -7)]
head(data)

kmean_clust = NbClust(data, min.nc=3, max.nc=5, method='kmeans')

##### Plot Similarity #####

distance = get_dist(data, method='euclidian')
fviz_dist(dist(data), gradient=list(low='#00AFBB', mid='white', high='#FC4E07'))

##### K-Means Clustering #####

clust_1 = NbClust(data, min.nc=2, max.nc=10, method='kmeans')

# Based on majority rule, 2 clusters is ideal. 

# Using Elbow method
fviz_nbclust(data, FUNcluster=kmeans, method='wss')

# With the elbow, we should use 3 or 4 clusters

##### 3 Clusters #####
km3 = kmeans(data, 3)

## Evaluate Quality of 3 Clusters ##
km3_stats = cluster.stats(dist(data), km3$cluster, silhouette = TRUE)

km3_stats$cluster.size

km3$centers
# notice how only aggriculture has a significant difference between the clusters
#  Industry and Manufacturing have the smallest differences

# Silhouettes above or near 0.50 indicate that the clusters are strong. 
km3_stats$clus.avg.silwidths

# Within cluster average distance by cluster
km3_stats$average.distance

# Between cluster average distnace by cluster
km3_stats$separation

## Evaluate Overall quality of the clustering

# Between cluster average distance
km3_stats$average.between

# Within cluster average distance
km3_stats$average.within

# Within cluster sum of squares
km3_stats$within.cluster.ss

# between cluster sum of squares
km3$betweenss

# Silhouette metric
km3_stats$avg.silwidth

## View Assignment of clusters
table(rownames(data), Cluster=km3$cluster)


##### kluster overview function #####
cluster_overview = function(data, kcluster){
  k_stats = cluster.stats(dist(data), kcluster$cluster, silhouette = TRUE)
  print('Cluster Centers')
  print(kcluster$centers)
  print('Cluster size')
  print(k_stats$cluster.size)
  print('Average Sil Widths')
  print(k_stats$clus.avg.silwidths)
  print('Within cluster average distance by cluster')
  print(k_stats$average.distance)
  print('Between cluster average distnace by cluster')
  print(k_stats$separation)
  print(' Evaluate Overall quality of the clustering')
  print( 'Between cluster average distance')
  print(k_stats$average.between)
  print(' Within cluster average distance')
  print(k_stats$average.within)
  print(' Within cluster sum of squares')
  print(k_stats$within.cluster.ss)
  print(' between cluster sum of squares')
  print(kcluster$betweenss)
  print('Silhouette metric')
  print(k_stats$avg.silwidth)
  print(' View Assignment of clusters ')
  print(table(rownames(data), Cluster=kcluster$cluster))
}

cluster_overview(data, km3)

##### Different Clusters #####
km4 = kmeans(data, 4)
cluster_overview(data, km4)

km5 = kmeans(data, 5)
cluster_overview(data, km5)

km8 = kmeans(data, 8)
cluster_overview(data, km8)


##### K Medoids #####

# k medoids recommends 3 clusters
kmedoids = NbClust(data, min.nc=2, max.nc=8, method='median')

# Elbow 

fviz_nbclust(data, pam, method='wss')

km3 = pam(data, 3, diss=FALSE, metric='euclidean')
cluster_overview(data, km3)

km4 = pam(data, 4, diss=FALSE, metric='euclidean')
cluster_overview(data, km4)

##### Hierarchical #####
nc = NbClust(data, min.nc=2, max.nc=10, method='complete')

hc = hclust(dist(data), method='complete')

plot(hc)

rect.hclust(hc, k=4)

hc$cluster = cutree(hc, k=4)

cluster_overview(data, hc)


##### Box Plots #####
# sets plots to print 2x1 per window
par(mfrow=c(2,1))
for (i in 1:(ncol(data))){
  boxplot(data[[i]]~hc$cluster, xlab='cluster', main=names(data)[i])
}

# resets plot to print 1 per window
par(mfrow=c(1,1))


##### Plotting #####

library(plotly)

Industry = data$Industry
Manufacturing = data$Manufacturing
Services = data$Services
Aggriculture = data$Aggriculture

plot_ly(x=Industry, y=Manufacturing, z=Services, mode='markers', color=Aggriculture)

#





#














#

#
