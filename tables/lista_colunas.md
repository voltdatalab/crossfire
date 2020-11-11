# Ocorrências - nomes e descrição das colunas

Na tabela abaixo, estão os nomes e descrição das colunas obtidas na requisição produzida pela função `get_fogocruzado`.

========================================================================================================================================================================================================
                  COLUNA                                                                                             VALOR                                                                              
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1             id_ocorrencia                                                                                      Id do registro                                                                         
2            local_ocorrencia                                                                                Endereço da ocorrência                                                                     
3          latitude_ocorrencia                                                                               Latitude da ocorrência                                                                     
4          longitude_ocorrencia                                                                             Longitude da ocorrência                                                                     
5            data_ocorrencia                                                                                   Data da ocorrência                                                                       
6            hora_ocorrencia                                                                                   Hora da ocorrência                                                                       
7      presen_agen_segur_ocorrencia                                                   Indicador se havia ou não presença de agentes de segurança no local                                               
8       qtd_morto_civil_ocorrencia                                                                  Quantidade de civis mortos na ocorrência                                                            
9    qtd_morto_agen_segur_ocorrencia                                                        Quantidade de agentes de segurança mortos na ocorrência                                                     
10     qtd_ferido_civil_ocorrencia                                                                 Quantidade de civis feridos na ocorrência                                                            
11   qtd_ferido_agen_segur_ocorrencia                                                       Quantidade de agentes de segurança feridos na ocorrência                                                    
12              estado_id                                                                                   Identificação do estado                                                                     
13              cidade_id                                                                                   Identificação da cidade                                                                     
14             nome_cidade                                                                                       Nome da cidade                                                                         
15           cod_ibge_cidade                                                                                    Código da cidade                                                                        
16           gentilico_cidade                                                                                 Gentílico da cidade                                                                       
17           populacao_cidade                                                                                 População da cidade                                                                       
18             area_cidade                                                                                       Área da cidade                                                                         
19        densidade_demo_cidade                                                                         Densidade demográfica da cidade                                                                 
20             nome_estado                                                                                       Nome do estado                                                                         
21              uf_estado                                                                                      Acrônimo do Estado                                                                       
22           cod_ibge_estado                                                                                    Código do estado                                                                        
23         homem_qtd_mortos_oc                                                                            Quantidade de homens mortos                                                                   
24         homem_qtd_feridos_oc                                                                           Quantidade de homens feridos                                                                  
25         mulher_qtd_mortos_oc                                                                          Quantidade de mulheres mortas                                                                  
26        mulher_qtd_feridos_oc                                                                          Quantidade de mulheres feridas                                                                 
27              chacina_oc                                                                 Indicador se ocorrência está relacionada a caso de chacina                                                   
28        chacina_qtd_mortos_oc                                                                      Quantidade de civis mortos na chacina                                                              
29    chacina_unidades_policiais_oc                                                  Unidades policiais envolvidas na ocorrência da chacina (quando houver)                                             
30        ag_seguranca_vitima_oc                                                                   Indicador de agentes de segurança baleados                                                           
31    ag_seguranca_mortos_status_oc                                             Indicador se a vítima estava em serviço, fora de serviço ou aposentada/exonerada                                        
32    ag_seguranca_feridos_status_oc                                            Indicador se a vítima estava em serviço, fora de serviço ou aposentada/exonerada                                        
33           bala_perdida_oc                                                            Indicador se ocorrência está relacionada a caso de bala perdida                                                 
34      bala_perdida_qtd_mortos_oc                                                               Quantidade de pessoas mortas por bala perdida                                                          
35     bala_perdida_qtd_feridos_oc                                                               Quantidade de pessoas feridas por bala perdida                                                         
36        interior_residencia_oc        Indicador de disparos de arma de fogo dentro de residências ou quintais. Ou ainda registros de tiros fora de residências, mas que atinjam o interior das mesmas.
37  interior_residencia_qtd_mortos_oc                                                 Quantidade de pessoas mortas por arma de fogo dentro de residências                                               
38  interior_residencia_qtd_feridos_oc                                                Quantidade de pessoas feridas por arma de fogo dentro de residências                                              
39         imediacao_ensino_oc                           Indicador de disparos de arma de fogo dentro de unidades de ensino (creches, escolas e universidades), ou nas suas imediações.                 
40    imediacao_ensino_qtd_mortos_oc                                                  Quantidade de pessoas mortas em unidades de ensino ou no seu entorno                                              
41   imediacao_ensino_qtd_feridos_oc                                                 Quantidade de pessoas feridas em unidades de ensino ou no seu entorno                                              
42          vitima_crianca_oc                                                   Indicador da existência de crianças (0 a 12 anos incompletos), entre os baleados                                        
43     vitima_crianca_qtd_mortos_oc                                                                      Quantidade de crianças mortas                                                                  
44     info_adicional_crianca_morto                                             Indicador de características adicionais da ocasião em que a vítima foi alvejada                                         
45    vitima_crianca_qtd_feridos_oc                                                                      Quantidade de crianças feridas                                                                 
46    info_adicional_crianca_ferido                                             Indicador de características adicionais da ocasião em que a vítima foi alvejada                                         
47        vitima_adolescente_oc                                              Indicador da existência de adolescentes (12 a 18 anos incompletos), entre os baleados                                      
48   vitima_adolescente_qtd_mortos_oc                                                                  Quantidade de adolescentes mortos                                                                
49   info_adicional_adolescente_morto                                           Indicador de características adicionais da ocasião em que a vítima foi alvejada                                         
50  vitima_adolescente_qtd_feridos_oc                                                                  Quantidade de adolescentes feridos                                                               
51  info_adicional_adolescente_ferido                                           Indicador de características adicionais da ocasião em que a vítima foi alvejada                                         
52           vitima_idoso_oc                                                       Indicador da existência de idosos (a partir de 60 anos), entre os baleados                                           
53      vitima_idoso_qtd_mortos_oc                                                                        Quantidade de idosos mortos                                                                   
54      info_adicional_idoso_morto                                              Indicador de características adicionais da ocasião em que a vítima foi alvejada                                         
55     vitima_idoso_qtd_feridos_oc                                                                        Quantidade de idosos feridos                                                                  
56    info_adicional_idoso_ferido_oc                                            Indicador de características adicionais da ocasião em que a vítima foi alvejada                                         
57       informacao_transporte_oc                                            Indicador de interrupção ou suspensão parcial da circulação de serviços de transporte                                      
58 descricao_transporte_interrompido_oc                                                 Nome do meio de transporte interrompido e ramal (quando cabível)                                                
59    data_interrupcao_transporte_oc                                                                         Horário de interrupção                                                                     
60     data_liberacao_transporte_oc                                                                           Horário de liberação                                                                      
61          informacao_via_oc                                                     Indicador de interrupção ou suspensão parcial da circulação em vias públicas                                          
62    descricao_via_interrompida_oc                                                                     Nome da via pública interrompida                                                                
63       data_interrupcao_via_oc                                                                             Horário de interrupção                                                                     
64        data_liberacao_via_oc                                                                               Horário de liberação                                                                      
65           outros_recortes                            lista de classificações de casos acompanhados pela equipe que não possuem campos específicos, chamados internamente de recortes                 
66           motivo_principal                                            motivo provável dos tiros - baseados em informações de imprensa, polícia ou fontes confiáveis                                  
67         motivo_complementar                                motivo provável dos tiros (caso haja mais de um) - baseados em informações de imprensa, polícia ou fontes confiáveis                      
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
