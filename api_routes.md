WEB API ROUTES
==============

## URI

GET /universe/{data_descriptor_id}/{term_id}
GET /{project_id}/{collection_id}/{term_id}

## Universe

GET /api/v1/universe/terms                                                 => get_all_terms_in_universe
GET /api/v1/universe/terms/{term_id}                                       => get_term_in_universe
GET /api/v1/universe/data_descriptors                                      => get_all_data_descriptors_in_universe
GET /api/v1/universe/data_descriptors/{data_descriptor_id}                 => get_data_descriptor_in_universe
GET /api/v1/universe/data_descriptors/{data_descriptor_id}/terms           => get_all_terms_in_data_descriptor
GET /api/v1/universe/data_descriptors/{data_descriptor_id}/terms/{term_id} => get_term_in_data_descriptor
GET /api/v1/universe/suggested/terms                                         => Backend only

## Projects

GET /api/v1/projects                                                          => get_all_projects
GET /api/v1/projects/{project_id}                                             => get_project
GET /api/v1/projects/{project_id}/terms                                       => get_all_terms_in_project
GET /api/v1/projects/{project_id}/terms/{term_id}                             => get_term_in_project
GET /api/v1/projects/{project_id}/collections                                 => get_all_collections_in_project
GET /api/v1/projects/{project_id}/collections/{collection_id}                 => get_collection_in_project
GET /api/v1/projects/{project_id}/collections/{collection_id}/terms           => get_all_terms_in_collection
GET /api/v1/projects/{project_id}/collections/{collection_id}/terms/{term_id} => get_term_in_collection

## Search

GET /api/v1/search/terms/universe?expression&data_descriptor_id       => find_terms_in_universe + find_terms_in_data_descriptor
GET /api/v1/search/terms/projects?expression&project_id&collection_id => find_terms_in_project + find_terms_in_collection
GET /api/v1/search/data_descriptors?expression                        => find_data_descriptors_in_universe
GET /api/v1/search/collections?expression&project_id                  => find_collections_in_project
GET /api/v1/search/items/universe?expression                          => find_items_in_universe
GET /api/v1/search/items/projects?expression&project_id               => find_items_in_project

## Cross search

GET /api/v1/cross/collections?project_id&data_descriptor_id   => get_collection_from_data_descriptor_in_all_projects +
                                                                 get_collection_from_data_descriptor_in_project
GET /api/v1/cross/terms?project_id&data_descriptor_id&term_id => get_term_from_universe_term_id_in_project +
                                                                 get_term_from_universe_term_id_in_all_projects

## Validation

GET /api/v1/validation/term?value&project_id&collection_id&term_id => valid_term_in_all_projects +
                                                                      valid_term_in_project +
                                                                      valid_term_in_collection +
                                                                      valid_term

## DRS

### Validation

GET /api/v1/apps/drs/{project_id}/validation/directory => validate_directory
GET /api/v1/apps/drs/{project_id}/validation/filename  => validate_file_name
GET /api/v1/apps/drs/{project_id}/validation/datasetid => validate_dataset_id

### Generation

POST /api/v1/apps/drs/{project_id}/generation/mapping/directory => generate_directory_from_mapping
POST /api/v1/apps/drs/{project_id}/generation/mapping/filename  => generate_file_name_from_mapping
POST /api/v1/apps/drs/{project_id}/generation/mapping/datasetid => generate_dataset_id_from_mapping
POST /api/v1/apps/drs/{project_id}/generation/terms/directory   => generate_directory_from_bag_of_terms
POST /api/v1/apps/drs/{project_id}/generation/terms/filename    => generate_file_name_from_bag_of_terms
POST /api/v1/apps/drs/{project_id}/generation/terms/datasetid   => generate_dataset_id_from_bag_of_terms
