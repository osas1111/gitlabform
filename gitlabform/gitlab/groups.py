from gitlabform.gitlab.core import GitLabCore, NotFoundException


class GitLabGroups(GitLabCore):

    def get_groups(self):
        """
        :return: sorted list of groups
        """
        result = self._make_requests_to_api("groups?all_available=true", paginated=True)
        return sorted(map(lambda x: x['full_path'], result))

    def get_projects(self, group):
        """
        :param group: group name
        :return: sorted list of strings "group/project_name". Note that only projects from "group" namespace are
                 returned, so if "group" (= members of this group) is also a member of some projects, they won't be
                 returned here.
        """
        try:
            projects = self._make_requests_to_api("groups/%s/projects?include_subgroups=true", group, paginated=True)
        except NotFoundException:
            projects = []

        all_project_and_groups = sorted(map(lambda x: x['path_with_namespace'], projects))

        project_and_groups_in_group_namespace = [x for x in all_project_and_groups if x.startswith(group + '/')]

        return project_and_groups_in_group_namespace
