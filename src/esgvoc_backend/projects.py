from fastapi import APIRouter

router = APIRouter(prefix="/projects")

"""
/projects                 => get_all_projects
/projects/find?project_id => find_project

/projects/terms                                  => get_all_terms_in_all_projects
/projects/terms/find?term_id                     => find_terms_in_all_projects
/projects/terms/valid?value                      => valid_term_in_all_projects
/projects/terms/cross?term_id&data_descriptor_id => find_terms_from_data_descriptor_in_all_projects

/projects/{project_id}/terms                                  => get_all_terms_in_project
/projects/{project_id}/terms/find?term_id                     => find_terms_in_project
/projects/{project_id}/terms/valid?value                      => valid_term_in_project
/projects/{project_id}/terms/cross?term_id&data_descriptor_id => find_terms_from_data_descriptor_in_project

/projects/{project_id}/collections                    => get_all_collections_in_project
/projects/{project_id}/collections/find?collection_id => find_collections_in_project

/projects/{project_id}/collections/{collection_id}/terms                     => get_all_terms_in_collection
/projects/{project_id}/collections/{collection_id}/terms/find?term_id        => find_terms_in_collection
/projects/{project_id}/collections/{collection_id}/terms/valid?value         => valid_term_in_collection
/projects/{project_id}/collections/{collection_id}/terms/valid?term_id&value => valid_term
"""
