import i18n from '@i18n';
import { FuseNavItemType } from '@fuse/core/FuseNavigation/types/FuseNavItemType';
import ar from './navigation-i18n/ar';
import en from './navigation-i18n/en';
import tr from './navigation-i18n/tr';

i18n.addResourceBundle('en', 'navigation', en);
i18n.addResourceBundle('tr', 'navigation', tr);
i18n.addResourceBundle('ar', 'navigation', ar);

/**
 * The navigationConfig object is an array of navigation items for the Fuse application.
 * Only includes items relevant to the AI Talent Matcher project.
 */
const navigationConfig: FuseNavItemType[] = [
	{
		id: 'dashboards',
		title: 'Dashboards',
		subtitle: 'Unique dashboard designs',
		type: 'group',
		icon: 'lucide:layout-dashboard',
		translate: 'DASHBOARDS',
		auth: null,
		children: [
			{
				id: 'dashboards.project',
				title: 'Project',
				type: 'item',
				icon: 'lucide:clipboard-check',
				url: '/dashboards/project',
				auth: null
			}
		]
	},
	{
		id: 'apps',
		title: 'Applications',
		subtitle: 'AI Talent Matcher',
		type: 'group',
		icon: 'lucide:box',
		translate: 'APPLICATIONS',
		auth: null,
		children: [
			{
				id: 'apps.talent-matcher',
				title: 'Talent Matcher',
				type: 'item',
				icon: 'lucide:users-round',
				url: '/apps/talent-matcher',
				auth: null,
				badge: {
					title: 'NEW'
				}
			}
		]
	}
];

export default navigationConfig;
